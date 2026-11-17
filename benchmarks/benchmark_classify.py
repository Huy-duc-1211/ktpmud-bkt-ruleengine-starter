"""Đo full public classify với audit thật và dữ liệu synthetic."""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
import tempfile
import time
from pathlib import Path
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from run_case import load_patient, read_cases  # noqa: E402
from rule_engine.classifier import classify  # noqa: E402

IDS = ('RULE-001', 'RULE-002', 'RULE-011', 'RULE-014', 'RULE-021')


def run(samples: int) -> dict:
    if samples < 1000:
        raise ValueError('Cần tối thiểu 1000 mẫu đo.')
    rows = {row['Test ID']: row for row in read_cases(ROOT / 'TEST_CASES.csv')}
    # Các fixture gốc 15 tuổi có BP nền null; đặt giá trị synthetic để đủ dữ liệu.
    patients = [dict(load_patient(rows[id_]), huyet_ap_tam_thu_nen=110) for id_ in IDS]
    if any(len(patient) != 9 or any(value is None for value in patient.values()) for patient in patients):
        raise ValueError('Dataset benchmark phải đủ 9 trường.')
    previous = os.environ.get('DR_MAY_DAY_AUDIT_PATH')
    try:
        with tempfile.TemporaryDirectory(prefix='rule-benchmark-') as tmp:
            path = Path(tmp).resolve() / 'audit.jsonl'
            os.environ['DR_MAY_DAY_AUDIT_PATH'] = str(path)
            for i in range(100):
                classify(patients[i % len(patients)])
            baseline = len(path.read_bytes().splitlines())
            timings = []
            for i in range(samples):
                start = time.perf_counter_ns()
                classify(patients[i % len(patients)])
                timings.append(time.perf_counter_ns() - start)
            records = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
            if baseline != 100 or len(records) != 100 + samples:
                raise RuntimeError('Số bản ghi audit không khớp; benchmark không hợp lệ.')
            for record in records:
                if (set(record) != {'Timestamp', 'User_UUID', 'Action_Type', 'Status'}
                    or record['Action_Type'] != 'CLASSIFY' or record['Status'] != 'SUCCESS'
                    or UUID(record['User_UUID']).version != 4):
                    raise RuntimeError('Bản ghi audit không hợp lệ; benchmark không hợp lệ.')
    finally:
        if previous is None:
            os.environ.pop('DR_MAY_DAY_AUDIT_PATH', None)
        else:
            os.environ['DR_MAY_DAY_AUDIT_PATH'] = previous
    ordered = sorted(timings)
    return {'python': platform.python_version(), 'os': platform.platform(),
            'dataset_ids': IDS, 'baseline_bp_synthetic': 110,
            'warmup': 100, 'sample_count': samples,
            'audit_records_warmup': baseline, 'audit_records_measured': len(records) - baseline,
            'uuid_scope': 'temporary per call', 'audit_io': 'append/write/flush/close; no fsync',
            'p50_ms': ordered[math.ceil(.5 * samples)-1]/1_000_000,
            'p95_ms': ordered[math.ceil(.95 * samples)-1]/1_000_000,
            'timings_ns': timings}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=1000)
    parser.add_argument('--output', type=Path, help='Lưu JSON timing; cần đường dẫn ngoài repo')
    args = parser.parse_args()
    if args.output and (not args.output.is_absolute() or args.output.resolve().is_relative_to(ROOT)):
        parser.error('--output phải là đường dẫn tuyệt đối ngoài repo')
    result = run(args.samples)
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key != 'timings_ns'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
