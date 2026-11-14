import json
import logging
import traceback
from contextvars import Context
from pathlib import Path

import pytest

from rule_engine.audit import AuditError, _session_uuid, audit_session
from rule_engine.classifier import classify


_CANARY = "SYNTHETIC_PRIVATE_CANARY"
_INTERNAL_CANARY = "SYNTHETIC_INTERNAL_ERROR"
_PRESSURE_CANARY = 97136485


@pytest.fixture
def internal_error_patient(monkeypatch):
    def fail(patient):
        raise RuntimeError(f"{_INTERNAL_CANARY} {patient['huyet_ap_tam_thu']}")

    monkeypatch.setattr("rule_engine.classifier._classify_valid", fail)
    return {"tuoi": 15, "huyet_ap_tam_thu": _PRESSURE_CANARY}


def _assert_no_payload(error, audit_file, capsys, caplog):
    assert error.__cause__ is None and error.__context__ is None
    output = capsys.readouterr()
    rendered = (
        str(error),
        "".join(traceback.format_exception(error, chain=True)),
        caplog.text,
        output.out,
        output.err,
        audit_file.read_text(encoding="utf-8") if audit_file.exists() else "",
    )
    for surface in rendered:
        for canary in (_CANARY, _INTERNAL_CANARY, str(_PRESSURE_CANARY)):
            assert canary not in surface
    assert output == ("", "")
    assert not caplog.records


def test_nested_sessions_restore_uuid_after_error_and_isolate_context(audit_records):
    with audit_session() as outer:
        classify({})
        with pytest.raises(TypeError), audit_session() as inner:
            classify({"tuoi": _CANARY})
        assert _session_uuid.get() == outer
        Context().run(classify, {})
        assert _session_uuid.get() == outer
        classify({})
    assert _session_uuid.get() is None
    classify({})
    assert _session_uuid.get() is None
    classify({})
    assert _session_uuid.get() is None
    records = audit_records("SUCCESS", "INVALID_INPUT", "SUCCESS", "SUCCESS", "SUCCESS", "SUCCESS")
    first, second, independent, restored, temporary1, temporary2 = [
        record["User_UUID"] for record in records
    ]
    assert first == restored == str(outer)
    assert second == str(inner)
    assert len({first, second, independent, temporary1, temporary2}) == 5


@pytest.mark.parametrize(("patient", "error_type"), [
    (None, TypeError),
    ({"tuoi": _CANARY}, TypeError),
    ({"tuoi": -1}, ValueError),
    ({_CANARY: True}, ValueError),
    ({"User_UUID": _CANARY}, ValueError),
    ({"audit_path": _CANARY}, ValueError),
])
def test_validation_audit_and_error_are_safe(patient, error_type, audit_file, audit_records):
    with pytest.raises(error_type) as caught:
        classify(patient)
    assert _session_uuid.get() is None
    assert _CANARY not in "".join(traceback.format_exception(caught.value))
    audit_records("INVALID_INPUT")
    assert _CANARY not in audit_file.read_text(encoding="utf-8")


@pytest.mark.parametrize("stage", ["mkdir", "open", "write", "short_write", "flush", "close"])
@pytest.mark.parametrize("scenario", ["valid", "invalid", "internal"])
def test_audit_failures_take_precedence(
    stage, scenario, request, audit_file, monkeypatch, capsys, caplog
):
    patient = {}
    if scenario == "invalid":
        patient = {"tuoi": _CANARY}
    elif scenario == "internal":
        patient = request.getfixturevalue("internal_error_patient")
    caplog.set_level(logging.DEBUG)

    def fail():
        raise OSError(_CANARY)

    real_mkdir = Path.mkdir
    real_open = Path.open
    attempted_statuses = []

    class FailingFile:
        def __enter__(self):
            return self

        def write(self, line):
            attempted_statuses.append(json.loads(line)["Status"])
            if stage == "write":
                fail()
            return len(line) - 1 if stage == "short_write" else len(line)

        def flush(self):
            if stage == "flush":
                fail()

        def __exit__(self, *_):
            if stage == "close":
                fail()

    def mkdir(path, *args, **kwargs):
        if path == audit_file.parent and stage == "mkdir":
            fail()
        return real_mkdir(path, *args, **kwargs)

    def open_file(path, *args, **kwargs):
        if path != audit_file:
            return real_open(path, *args, **kwargs)
        if stage == "open":
            fail()
        return FailingFile()

    with monkeypatch.context() as patches:
        patches.setattr(Path, "mkdir", mkdir)
        patches.setattr(Path, "open", open_file)
        with pytest.raises(AuditError, match="^Không thể hoàn tất bản ghi audit\\.$") as caught:
            classify(patient)
        assert _session_uuid.get() is None
        with audit_session() as session:
            with pytest.raises(AuditError):
                classify(patient)
            assert _session_uuid.get() == session
        assert _session_uuid.get() is None
    expected_status = {"valid": "SUCCESS", "invalid": "INVALID_INPUT", "internal": "INTERNAL_ERROR"}
    if stage in {"mkdir", "open"}:
        assert attempted_statuses == []
    else:
        assert attempted_statuses == [expected_status[scenario]] * 2
    _assert_no_payload(caught.value, audit_file, capsys, caplog)


def test_audit_closes_real_file_before_classify_returns(audit_file, audit_records, monkeypatch):
    events = []
    real_open = Path.open

    class ObservedFile:
        def __init__(self, file):
            self.file = file

        def __enter__(self):
            self.file.__enter__()
            return self

        def write(self, line):
            events.append("write")
            return self.file.write(line)

        def flush(self):
            events.append("flush")
            self.file.flush()

        def __exit__(self, *args):
            self.file.__exit__(*args)
            assert self.file.closed
            events.append("close")

    def observe_open(path, *args, **kwargs):
        file = real_open(path, *args, **kwargs)
        if path == audit_file:
            events.append("open")
            return ObservedFile(file)
        return file

    with monkeypatch.context() as patches:
        patches.setattr(Path, "open", observe_open)
        assert classify({})["muc_do"] == "THEO_DOI"
    assert events == ["open", "write", "flush", "close"]
    audit_records("SUCCESS")


def test_absolute_override_survives_working_directory_change(audit_file, audit_records, monkeypatch):
    elsewhere = audit_file.parent / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    classify({})
    assert not list(elsewhere.iterdir())
    audit_records("SUCCESS")


def test_default_path_is_per_run_and_independent_of_cwd(audit_file, monkeypatch):
    from rule_engine.audit import _audit_path

    monkeypatch.delenv("DR_MAY_DAY_AUDIT_PATH")
    monkeypatch.setattr(Path, "home", lambda: audit_file.parent / "fake-home")
    first_path = _audit_path()
    assert first_path.is_relative_to(Path.home())
    classify({})
    elsewhere = audit_file.parent / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    classify({})
    assert _audit_path() == first_path
    assert len(first_path.read_text(encoding="utf-8").splitlines()) == 2
    assert not list(elsewhere.iterdir())


def test_relative_path_and_repository_paths_fail_closed(audit_file, monkeypatch):
    checkout = Path(__file__).resolve().parents[1]
    other_repo = audit_file.parent / "other-repository"
    (other_repo / ".git").mkdir(parents=True)
    for path in ("audit.jsonl", checkout / "audit.jsonl", other_repo / "audit.jsonl"):
        monkeypatch.setenv("DR_MAY_DAY_AUDIT_PATH", str(path))
        with pytest.raises(AuditError):
            classify({})
    assert not (other_repo / "audit.jsonl").exists()


def test_unexpected_rule_error_records_internal_error_without_payload(
    internal_error_patient, audit_file, audit_records, capsys, caplog
):
    caplog.set_level(logging.DEBUG)
    with audit_session() as session:
        with pytest.raises(RuntimeError, match="^Không thể hoàn tất phân loại\\.$") as caught:
            classify(internal_error_patient)
        assert _session_uuid.get() == session
    assert _session_uuid.get() is None
    assert type(caught.value) is RuntimeError
    record, = audit_records("INTERNAL_ERROR")
    assert record["User_UUID"] == str(session)
    _assert_no_payload(caught.value, audit_file, capsys, caplog)
