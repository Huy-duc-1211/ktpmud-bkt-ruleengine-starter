"""Chạy classify() với một ca giả lập trong CSV."""

import argparse
import csv
import json
import math
from pathlib import Path

from rule_engine.classifier import classify


ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "TEST_CASES.csv"
FIXTURES_DIR = ROOT / "tests" / "fixtures"
NONFINITE_REGISTRY = FIXTURES_DIR / "NONFINITE_INPUTS.json"
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


def _run_case(cases, case_id):
    matching = [case for case in cases if case.get("Test ID") == case_id]
    if len(matching) != 1:
        raise ValueError(f"Cần đúng một dòng có mã {case_id}, tìm thấy {len(matching)}.")
    case, = matching
    try:
        patient = load_patient(case)
    except (OSError, csv.Error, KeyError, TypeError, ValueError):
        raise ValueError("Không đọc được ca từ CSV. Kiểm tra cấu trúc file.") from None

    try:
        result = classify(patient)
    except (RuntimeError, TypeError, ValueError) as error:
        print(json.dumps(
            {"exception_class": type(error).__name__, "message": str(error)},
            ensure_ascii=False,
            indent=2,
        ))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Chạy classify() theo mã ca trong CSV giả lập.")
    parser.add_argument("case_id", nargs="?", help="Mã ca, ví dụ MISS-009")
    parser.add_argument("--csv", type=Path, help="Đường dẫn tới CSV ca test")
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
    if not csv_path.is_file():
        print("null")
        return 0

    try:
        cases = read_cases(csv_path)
    except (OSError, csv.Error, ValueError):
        parser.error("Không đọc được file CSV. Kiểm tra đường dẫn và cấu trúc file.")

    while True:
        case_id = args.case_id
        if interactive:
            try:
                case_id = input("Nhập mã ca (ví dụ MISS-009, nhập END để kết thúc): ")
            except (EOFError, KeyboardInterrupt):
                return 0
        case_id = case_id.strip().upper()
        if case_id == "END":
            return 0
        if not case_id:
            if interactive:
                continue
            return 0

        try:
            status = _run_case(cases, case_id)
        except ValueError as error:
            if not interactive:
                parser.error(str(error))
            print(error)
        else:
            if not interactive:
                return status


if __name__ == "__main__":
    raise SystemExit(main())
