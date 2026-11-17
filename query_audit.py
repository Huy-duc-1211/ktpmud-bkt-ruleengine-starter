"""Đọc bản ghi audit hợp lệ và báo vị trí các dòng bị bỏ qua."""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import UUID


def _unique_object(pairs):
    record = dict(pairs)
    if len(record) != len(pairs):
        raise ValueError("Bản ghi audit có khóa trùng.")
    return record


def _parse_record(line: bytes) -> dict[str, str]:
    record = json.loads(line.decode("utf-8"), object_pairs_hook=_unique_object)
    if (
        not isinstance(record, dict)
        or record.keys() != {"Timestamp", "User_UUID", "Action_Type", "Status"}
        or not all(isinstance(value, str) for value in record.values())
        or record["Action_Type"] != "CLASSIFY"
        or record["Status"] not in {"SUCCESS", "INVALID_INPUT", "INTERNAL_ERROR"}
    ):
        raise ValueError("Sai cấu trúc bản ghi audit.")

    timestamp = record["Timestamp"]
    if timestamp.endswith("Z"):
        timestamp = timestamp[:-1] + "+00:00"
    if datetime.fromisoformat(timestamp).utcoffset() != timedelta(0):
        raise ValueError("Timestamp của audit phải dùng UTC.")
    if UUID(record["User_UUID"]).version != 4:
        raise ValueError("User_UUID phải là UUID phiên giả lập.")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Đọc file audit JSONL, bỏ qua các dòng lỗi.")
    parser.add_argument("path", type=Path, help="Đường dẫn file audit JSONL")
    args = parser.parse_args(argv)

    count = 0
    skipped = []
    try:
        with args.path.open("rb") as audit_file:
            for number, line in enumerate(audit_file, start=1):
                try:
                    record = _parse_record(line)
                except (ValueError, RecursionError):
                    skipped.append(number)
                    continue
                print(json.dumps(record))
                count += 1
    except OSError:
        print("Không thể đọc hết file audit.", file=sys.stderr)
        return 1

    locations = ", ".join(map(str, skipped)) if skipped else "không có"
    print(
        f"Đọc được {count} bản ghi, bỏ qua {len(skipped)} dòng lỗi, "
        f"lỗi tại các dòng: {locations}.",
        file=sys.stderr,
    )
    return 3 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
