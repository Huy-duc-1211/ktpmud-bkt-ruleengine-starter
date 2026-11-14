"""Ghi audit JSONL cho từng lần phân loại dữ liệu giả lập."""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Literal
from uuid import UUID, uuid4


class AuditError(RuntimeError):
    """Không thể hoàn tất bản ghi audit bắt buộc."""


_session_uuid: ContextVar[UUID | None] = ContextVar("audit_session_uuid", default=None)
_run_id = uuid4()
_checkout = Path(__file__).resolve().parents[1]


@contextmanager
def audit_session() -> Iterator[UUID]:
    """Tạo UUID giả lập dùng chung cho các lần gọi trong phiên."""
    user_uuid = uuid4()
    token = _session_uuid.set(user_uuid)
    try:
        yield user_uuid
    finally:
        _session_uuid.reset(token)


@contextmanager
def _audit_call() -> Iterator[UUID]:
    user_uuid = _session_uuid.get()
    if user_uuid is not None:
        yield user_uuid
    else:
        with audit_session() as temporary_uuid:
            yield temporary_uuid


def _audit_path() -> Path:
    override = os.environ.get("DR_MAY_DAY_AUDIT_PATH")
    if override is None:
        path = Path.home() / ".173820_n27" / "dr_may_day" / "runs" / str(_run_id) / "audit.jsonl"
    else:
        path = Path(override)
    if not path.is_absolute():
        raise ValueError("Cần đường dẫn audit tuyệt đối.")
    path = path.resolve()
    if path.is_relative_to(_checkout) or any((parent / ".git").exists() for parent in path.parents):
        raise ValueError("Cần lưu audit ngoài repository.")
    return path


def _write_record(
    user_uuid: UUID, status: Literal["SUCCESS", "INVALID_INPUT", "INTERNAL_ERROR"]
) -> None:
    record = {
        "Timestamp": datetime.now(timezone.utc).isoformat(),
        "User_UUID": str(user_uuid),
        "Action_Type": "CLASSIFY",
        "Status": status,
    }
    try:
        path = _audit_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as output:
            line = json.dumps(record) + "\n"
            if output.write(line) != len(line):
                raise OSError("Bản ghi audit chưa được ghi đầy đủ.")
            output.flush()
    except (OSError, ValueError, RuntimeError):
        pass
    else:
        return
    raise AuditError("Không thể hoàn tất bản ghi audit.") from None
