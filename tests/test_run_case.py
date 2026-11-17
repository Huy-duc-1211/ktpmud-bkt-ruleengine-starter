import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest


RUN_CASE = Path(__file__).resolve().parents[1] / "run_case.py"


def run_case(*args, stdin=""):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(RUN_CASE), *args],
        input=stdin,
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )


def read_export(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


@pytest.mark.parametrize("interactive", [False, True], ids=["cli", "interactive"])
@pytest.mark.parametrize("path_kind", ["missing-file", "directory"])
def test_rejects_path_without_csv(tmp_path, interactive, path_kind):
    csv_path = tmp_path / "does-not-exist.csv" if path_kind == "missing-file" else tmp_path
    if interactive:
        result = run_case(stdin=f"{csv_path}\n")
    else:
        result = run_case("MISS-009", "--csv", str(csv_path))

    assert result.returncode == 1
    assert f"Không tìm thấy file CSV tại đường dẫn {csv_path}." in result.stderr
    assert "null" not in result.stdout
    assert "Nhập mã ca" not in result.stdout
    if interactive:
        assert "Nhập đường dẫn file CSV" in result.stdout


@pytest.mark.parametrize(("case_id", "status"), [("MISS-009", 0), ("INV-005", 1)])
def test_cli_exports_the_printed_result(tmp_path, case_id, status):
    output = tmp_path / "kết quả.csv"
    result = run_case(case_id, "--export-csv", str(output))

    assert result.returncode == status
    expected = dict.fromkeys(("muc_do", "rule_id", "ly_do", "exception_class", "message"), "")
    expected.update(json.loads(result.stdout), test_id=case_id)
    assert read_export(output) == [expected]


@pytest.mark.parametrize("export_option", ["prompt", "flag"])
def test_interactive_exports_multiple_results(tmp_path, export_option):
    output = tmp_path / "results.csv"
    stdin = "TEST_CASES.csv\nMISS-009\nNO-SUCH-CASE\nINV-005\n"
    if export_option == "prompt":
        result = run_case(stdin=f"{stdin}/CSV\n{output}\nMISS-013\nEND\n")
        assert result.stdout.count('"muc_do"') == 2
    else:
        result = run_case("--export-csv", str(output), stdin=f"{stdin}END\n")

    assert result.returncode == 0
    success, rejected = read_export(output)
    assert success["test_id"] == "MISS-009"
    assert success["muc_do"] == "PHAN_VE"
    assert success["rule_id"] == "R01-PV"
    assert rejected["test_id"] == "INV-005"
    assert rejected["exception_class"] == "ValueError"


def test_export_does_not_overwrite_existing_file(tmp_path):
    output = tmp_path / "results.csv"
    output.write_bytes(b"existing contents")

    result = run_case("MISS-009", "--export-csv", str(output))

    assert result.returncode == 1
    assert "đã tồn tại" in result.stderr
    assert output.read_bytes() == b"existing contents"
