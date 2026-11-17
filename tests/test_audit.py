import json
import logging
import traceback
from contextvars import Context
from pathlib import Path

import pytest

import query_audit
import rule_engine.audit as audit
import rule_engine.classifier as classifier
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

        def seek(self, *_):
            return 0  # File giả lập đang trống.

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

        def __getattr__(self, name):
            return getattr(self.file, name)

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


@pytest.mark.parametrize("error_type", [KeyError, TypeError, ValueError])
def test_unexpected_validator_error_is_internal(
    error_type, audit_file, audit_records, monkeypatch, capsys, caplog
):
    caplog.set_level(logging.DEBUG)

    def fail(patient):
        raise error_type(f"{_INTERNAL_CANARY} {patient['huyet_ap_tam_thu']}")

    monkeypatch.setattr(classifier, "_validate", fail)
    with pytest.raises(RuntimeError, match=r"^Không thể hoàn tất phân loại\.$") as caught:
        classify({"tuoi": 15, "huyet_ap_tam_thu": _PRESSURE_CANARY})
    assert type(caught.value) is RuntimeError
    assert _session_uuid.get() is None
    audit_records("INTERNAL_ERROR")
    _assert_no_payload(caught.value, audit_file, capsys, caplog)


@pytest.mark.parametrize("stage", ["record", "path", "open", "check_tail"])
@pytest.mark.parametrize("scenario", ["valid", "invalid", "validator", "rule"])
def test_unexpected_audit_error_is_safe(
    stage, scenario, audit_file, monkeypatch, capsys, caplog
):
    caplog.set_level(logging.DEBUG)
    patient = {"tuoi": 15, "huyet_ap_tam_thu": _PRESSURE_CANARY}
    if scenario == "invalid":
        patient["tuoi"] = _CANARY
    elif scenario in {"validator", "rule"}:
        def fail_classification(_patient):
            raise ValueError(_INTERNAL_CANARY)

        helper = "_validate" if scenario == "validator" else "_classify_valid"
        monkeypatch.setattr(classifier, helper, fail_classification)

    def fail_audit(*_):
        raise KeyError(_CANARY)

    if stage == "record":
        class BrokenClock:
            now = staticmethod(fail_audit)

        monkeypatch.setattr(audit, "datetime", BrokenClock)
    elif stage == "path":
        monkeypatch.setattr(audit, "_audit_path", fail_audit)
    elif stage == "open":
        real_open = Path.open

        def fail_open(path, *args, **kwargs):
            if path == audit_file:
                fail_audit()
            return real_open(path, *args, **kwargs)

        monkeypatch.setattr(Path, "open", fail_open)
    else:
        monkeypatch.setattr(audit, "_separator_before_append", fail_audit)
    with audit_session() as session:
        with pytest.raises(AuditError, match=r"^Không thể hoàn tất bản ghi audit\.$") as caught:
            classify(patient)
        assert _session_uuid.get() == session
    assert _session_uuid.get() is None
    _assert_no_payload(caught.value, audit_file, capsys, caplog)


@pytest.mark.parametrize("ending", [b"", b"\n", b"\r\n"], ids=["no-newline", "lf", "crlf"])
def test_append_preserves_complete_audit_line(audit_file, audit_records, ending):
    audit_file.touch()
    classify({})
    first_line = audit_file.read_bytes()
    assert first_line.count(b"\n") == 1 and first_line.endswith(b"\n")
    before = first_line + first_line.rstrip(b"\n") + ending
    audit_file.write_bytes(before)

    assert classify({})["muc_do"] == "THEO_DOI"
    separator = b"" if ending else b"\n"
    contents = audit_file.read_bytes()
    assert contents.startswith(before + separator)
    assert contents.count(b"\n") == 3 and contents.endswith(b"\n")
    audit_records("SUCCESS", "SUCCESS", "SUCCESS")


@pytest.mark.parametrize("tail", [
    b'{"Timestamp":',
    b'{"Timestamp":\n',
    b'{"Timestamp":"2026-11-16T08:00:00Z"}',
    b"\xff",
], ids=["unfinished", "malformed-with-newline", "wrong-fields", "invalid-utf8"])
def test_bad_audit_tail_is_preserved_as_its_own_line(audit_file, tail, capsys):
    classify({})
    classify({})
    before = audit_file.read_bytes() + tail
    audit_file.write_bytes(before)

    assert classify({})["muc_do"] == "THEO_DOI"
    separator = b"" if tail.endswith(b"\n") else b"\n"
    contents = audit_file.read_bytes()
    assert contents.startswith(before + separator)
    assert contents.endswith(b"\n") and contents.count(b"\n") == 4
    assert _session_uuid.get() is None
    assert query_audit.main([str(audit_file)]) == 3
    result = capsys.readouterr()
    assert [json.loads(line)["Status"] for line in result.out.splitlines()] == ["SUCCESS"] * 3
    assert result.err == "Đọc được 3 bản ghi, bỏ qua 1 dòng lỗi, lỗi tại các dòng: 3.\n"


@pytest.mark.parametrize("raise_after_write", [False, True], ids=["short-write", "write-error"])
def test_partial_write_to_real_file_keeps_next_record_readable(
    raise_after_write, audit_file, audit_records, monkeypatch, capsys
):
    classify({})
    audit_records("SUCCESS")
    original = audit_file.read_bytes()
    real_open = Path.open

    class PartialWriter:
        def __init__(self, file):
            self.file = file

        def __enter__(self):
            self.file.__enter__()
            return self

        def __exit__(self, *args):
            return self.file.__exit__(*args)

        def __getattr__(self, name):
            return getattr(self.file, name)

        def write(self, payload):
            count = self.file.write(payload[:len(payload) // 2])
            self.file.flush()
            if raise_after_write:
                raise OSError(_CANARY)
            return count

    def open_partial(path, *args, **kwargs):
        file = real_open(path, *args, **kwargs)
        return PartialWriter(file) if path == audit_file else file

    with monkeypatch.context() as patches:
        patches.setattr(Path, "open", open_partial)
        with pytest.raises(AuditError):
            classify({})

    damaged = audit_file.read_bytes()
    assert damaged.startswith(original) and len(damaged) > len(original)
    assert not damaged.endswith(b"\n")
    assert classify({})["muc_do"] == "THEO_DOI"
    contents = audit_file.read_bytes()
    original_line, _, new_line = contents.splitlines()
    assert contents.startswith(damaged + b"\n") and contents.endswith(b"\n")
    assert _session_uuid.get() is None

    assert query_audit.main([str(audit_file)]) == 3
    result = capsys.readouterr()
    assert [json.loads(line) for line in result.out.splitlines()] == [
        json.loads(original_line), json.loads(new_line)
    ]
    assert json.loads(new_line)["Status"] == "SUCCESS"
    assert result.err == "Đọc được 2 bản ghi, bỏ qua 1 dòng lỗi, lỗi tại các dòng: 2.\n"
    assert audit_file.read_bytes() == contents


def test_query_audit_reports_multiple_bad_lines_and_reads_valid_eof(audit_file, capsys):
    classify({})
    valid = audit_file.read_bytes()
    invalid = json.loads(valid)
    invalid["User_UUID"] = _CANARY
    before = valid + b"\xff\n" + valid + json.dumps(invalid).encode() + b"\n" + valid.rstrip(b"\n")
    audit_file.write_bytes(before)

    assert query_audit.main([str(audit_file)]) == 3
    result = capsys.readouterr()
    assert [json.loads(line) for line in result.out.splitlines()] == [json.loads(valid)] * 3
    assert result.err == "Đọc được 3 bản ghi, bỏ qua 2 dòng lỗi, lỗi tại các dòng: 2, 4.\n"
    assert _CANARY not in result.out + result.err
    assert audit_file.read_bytes() == before


def test_query_audit_reports_empty_and_missing_file(audit_file, capsys):
    assert query_audit.main([str(audit_file)]) == 1
    assert capsys.readouterr() == ("", "Không thể đọc hết file audit.\n")

    audit_file.touch()
    assert query_audit.main([str(audit_file)]) == 0
    assert capsys.readouterr() == (
        "", "Đọc được 0 bản ghi, bỏ qua 0 dòng lỗi, lỗi tại các dòng: không có.\n"
    )


def test_query_audit_skips_duplicate_keys_and_preserves_surrounding_records(audit_file, capsys):
    classify({})
    with pytest.raises(TypeError):
        classify({"tuoi": "invalid"})
    first, last = audit_file.read_bytes().splitlines(keepends=True)
    expected_records = [json.loads(first), json.loads(last)]
    assert query_audit.main([str(audit_file)]) == 0
    clean = capsys.readouterr()
    assert [json.loads(line) for line in clean.out.splitlines()] == expected_records
    assert clean.err == "Đọc được 2 bản ghi, bỏ qua 0 dòng lỗi, lỗi tại các dòng: không có.\n"

    duplicate = first.replace(b'"Status": "SUCCESS"', b'"Status": "INVALID_INPUT", "Status": "SUCCESS"')
    contents = first + duplicate + last
    audit_file.write_bytes(contents)

    assert query_audit.main([str(audit_file)]) == 3
    output = capsys.readouterr()
    assert [json.loads(line) for line in output.out.splitlines()] == expected_records
    assert output.err == "Đọc được 2 bản ghi, bỏ qua 1 dòng lỗi, lỗi tại các dòng: 2.\n"
    assert audit_file.read_bytes() == contents
