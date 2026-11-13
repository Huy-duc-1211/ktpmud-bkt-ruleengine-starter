import json
from datetime import datetime, timedelta
from pathlib import Path
from uuid import UUID

import pytest

from rule_engine.audit import _session_uuid


@pytest.fixture(autouse=True)
def audit_file(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    path = (tmp_path / "audit.jsonl").resolve()
    assert not path.is_relative_to(root)
    monkeypatch.setenv("DR_MAY_DAY_AUDIT_PATH", str(path))
    token = _session_uuid.set(None)
    try:
        yield path
    finally:
        _session_uuid.reset(token)


@pytest.fixture
def audit_records(audit_file):
    def read_records(*expected_statuses):
        records = [
            json.loads(line) for line in audit_file.read_text(encoding="utf-8").splitlines()
        ] if audit_file.exists() else []
        assert len(records) == len(expected_statuses)
        for record, status in zip(records, expected_statuses):
            assert set(record) == {"Timestamp", "User_UUID", "Action_Type", "Status"}
            assert datetime.fromisoformat(record["Timestamp"]).utcoffset() == timedelta(0)
            assert UUID(record["User_UUID"]).version == 4
            assert record["Action_Type"] == "CLASSIFY"
            assert record["Status"] == status
        return records

    return read_records
