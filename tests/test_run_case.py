import subprocess
import sys
from pathlib import Path

import pytest


RUN_CASE = Path(__file__).resolve().parents[1] / "run_case.py"


@pytest.mark.parametrize("interactive", [False, True], ids=["cli", "interactive"])
@pytest.mark.parametrize("path_kind", ["missing-file", "directory"])
def test_rejects_path_without_csv(tmp_path, interactive, path_kind):
    csv_path = tmp_path / "does-not-exist.csv" if path_kind == "missing-file" else tmp_path
    command = [sys.executable, "-X", "utf8", str(RUN_CASE)]
    if not interactive:
        command.extend(["MISS-009", "--csv", str(csv_path)])

    result = subprocess.run(
        command,
        input=f"{csv_path}\n" if interactive else "",
        capture_output=True,
        encoding="utf-8",
        timeout=10,
    )

    assert result.returncode == 1
    assert f"Không tìm thấy file CSV tại đường dẫn {csv_path}." in result.stderr
    assert "null" not in result.stdout
    assert "Nhập mã ca" not in result.stdout
    if interactive:
        assert "Nhập đường dẫn file CSV" in result.stdout
