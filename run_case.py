"""Chạy classify() với ca giả lập và xuất kết quả ra CSV khi cần."""

import argparse
import csv
import json
import math
import sys
from pathlib import Path

from rule_engine.classifier import classify


ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "TEST_CASES.csv"
FIXTURES_DIR = ROOT / "tests" / "fixtures"
NONFINITE_REGISTRY = FIXTURES_DIR / "NONFINITE_INPUTS.json"
RESULT_COLUMNS = ("test_id", "muc_do", "rule_id", "ly_do", "exception_class", "message")
_FLOAT_VALUES = {
    "NAN": math.nan,
    "POSITIVE_INFINITY": math.inf,
    "NEGATIVE_INFINITY": -math.inf,
}


def _unique_object(pairs):
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise ValueError("JSON có khóa trùng.")
    return obj


def _reject_constant(token):
    raise ValueError(f"Hằng JSON không hợp lệ: {token}")


def read_json(source):
    return json.loads(source, object_pairs_hook=_unique_object, parse_constant=_reject_constant)


def read_cases(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def load_patient(case):
    data = read_json(case["Input"])
    encoding = case["Fixture encoding"]
    if encoding == "json":
        return data
    if encoding != "fixture_ref" or data != {"fixture_ref": case["Test ID"]}:
        raise ValueError("Khai báo fixture không hợp lệ.")

    registry = read_json(NONFINITE_REGISTRY.read_text(encoding="utf-8"))
    if (
        set(registry) != {"schema_version", "kind", "base_patient", "fixtures"}
        or registry["schema_version"] != 1
        or registry["kind"] != "nonfinite_age_fixture_registry"
    ):
        raise ValueError("Sai cấu trúc file fixture NaN/Infinity.")

    fixture = registry["fixtures"][data["fixture_ref"]]
    if set(fixture) != {"override_field", "float_token"} or fixture["override_field"] != "tuoi":
        raise ValueError("Sai cấu trúc fixture NaN/Infinity.")

    return dict(registry["base_patient"], tuoi=_FLOAT_VALUES[fixture["float_token"]])


def _classify_case(cases, case_id):
    matching = [case for case in cases if case.get("Test ID") == case_id]
    if len(matching) != 1:
        raise ValueError(f"Cần đúng một dòng có mã {case_id}, tìm thấy {len(matching)}.")
    case, = matching
    try:
        patient = load_patient(case)
    except (OSError, csv.Error, KeyError, TypeError, ValueError):
        raise ValueError("Không đọc được ca từ CSV. Kiểm tra cấu trúc file.") from None

    try:
        return classify(patient), 0
    except (RuntimeError, TypeError, ValueError) as error:
        return {"exception_class": type(error).__name__, "message": str(error)}, 1


def _csv_list_separator():
    if sys.platform != "win32":
        return ","

    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International") as key:
            separator, _ = winreg.QueryValueEx(key, "sList")
    except OSError:
        return ","
    return separator if separator in (",", ";") else ","


def _export_csv(path, results):
    if path.suffix.lower() != ".csv" and path.name:
        path = path.with_name(f"{path.name}.csv")
    try:
        with path.open("x", encoding="utf-8-sig", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=RESULT_COLUMNS, delimiter=_csv_list_separator())
            writer.writeheader()
            writer.writerows(results)
    except FileExistsError:
        print(f"File {path} đã tồn tại. Hãy chọn tên khác.", file=sys.stderr)
        return False
    except (OSError, csv.Error, ValueError):
        print(f"Không ghi được file CSV tại đường dẫn {path}.", file=sys.stderr)
        return False

    print(f"Đã xuất {len(results)} kết quả vào {path}.", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(description="Chạy classify() theo mã ca trong CSV giả lập.")
    parser.add_argument("case_id", nargs="?", help="Mã ca, ví dụ MISS-009")
    parser.add_argument("--csv", type=Path, help="Đường dẫn tới CSV ca test")
    parser.add_argument("--export-csv", type=Path, help="Đường dẫn tới file CSV kết quả mới")
    args = parser.parse_args()
    interactive = args.case_id is None
    csv_path = args.csv
    if csv_path is None and interactive:
        try:
            entered = input("Nhập đường dẫn file CSV (ví dụ TEST_CASES.csv): ").strip()
        except (EOFError, KeyboardInterrupt):
            return 0
        if entered.lower().startswith("cd "):
            entered = entered[3:].strip()
        if len(entered) >= 2 and entered[0] in "\"'" and entered[0] == entered[-1]:
            entered = entered[1:-1]
        csv_path = ROOT / entered
    if csv_path is None:
        csv_path = DEFAULT_CSV

    try:
        if not csv_path.is_file():
            raise FileNotFoundError
        cases = read_cases(csv_path)
    except (FileNotFoundError, IsADirectoryError):
        print(f"Không tìm thấy file CSV tại đường dẫn {csv_path}.", file=sys.stderr)
        return 1
    except (OSError, csv.Error, ValueError):
        parser.error("Không đọc được file CSV. Kiểm tra đường dẫn và cấu trúc file.")

    results = []
    exit_status = 0
    while True:
        case_id = args.case_id
        if interactive:
            try:
                case_id = input("Nhập mã ca (ví dụ MISS-009, /CSV để xuất, END để kết thúc): ")
                if case_id.strip().upper() == "/CSV":
                    if results:
                        destination = input("Nhập đường dẫn file CSV kết quả: ").strip()
                        if destination and not _export_csv(Path(destination), results):
                            exit_status = 1
                    else:
                        print("Chưa có kết quả để xuất.")
                    continue
            except (EOFError, KeyboardInterrupt):
                break
        case_id = case_id.strip().upper()
        if case_id == "END":
            break
        if not case_id:
            if interactive:
                continue
            return 0

        try:
            result, status = _classify_case(cases, case_id)
        except ValueError as error:
            if not interactive:
                parser.error(str(error))
            print(error)
            continue

        print(json.dumps(result, ensure_ascii=False, indent=2))
        results.append({"test_id": case_id, **result})
        if status:
            exit_status = status
        if not interactive:
            break

    if args.export_csv is not None and results:
        if not _export_csv(args.export_csv, results):
            return 1
    return exit_status


if __name__ == "__main__":
    if sys.platform == "win32":
        for stream in (sys.stdin, sys.stdout, sys.stderr):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
