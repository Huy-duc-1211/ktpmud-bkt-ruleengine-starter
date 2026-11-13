"""Phân loại dữ liệu giả lập theo Decision Table V1 của Track A."""
from __future__ import annotations

from enum import Enum
from itertools import product
from math import isfinite
from typing import TypedDict

from .audit import _audit_call, _write_record


class PatientInput(TypedDict, total=False):
    tuoi: float | None
    huyet_ap_tam_thu: int | None
    huyet_ap_tam_thu_nen: int | None
    co_di_nguyen_nghi_ngo: bool | None
    di_nguyen_qua_duong_hit: bool | None
    co_ton_thuong_da_niem_mac: bool | None
    co_trieu_chung_ho_hap: bool | None
    co_trieu_chung_tuan_hoan: bool | None
    co_trieu_chung_tieu_hoa_nang: bool | None


class ClassificationResult(TypedDict):
    muc_do: str
    rule_id: str | None
    ly_do: str


_BOOLEAN_FIELDS = {
    "co_di_nguyen_nghi_ngo": "dị nguyên nghi ngờ",
    "di_nguyen_qua_duong_hit": "đường hít",
    "co_ton_thuong_da_niem_mac": "tổn thương da hoặc niêm mạc",
    "co_trieu_chung_ho_hap": "triệu chứng hô hấp",
    "co_trieu_chung_tuan_hoan": "triệu chứng tuần hoàn",
    "co_trieu_chung_tieu_hoa_nang": "triệu chứng tiêu hóa nặng",
}
_RULE_IDS = ("R01-PV", "R02-PV", "R03-PV")


class _Truth(Enum):
    TRUE = True
    FALSE = False
    UNKNOWN = None


def _and(left: _Truth, right: _Truth) -> _Truth:
    if left is _Truth.FALSE or right is _Truth.FALSE:
        return _Truth.FALSE
    if left is _Truth.TRUE and right is _Truth.TRUE:
        return _Truth.TRUE
    return _Truth.UNKNOWN


def _or(left: _Truth, right: _Truth) -> _Truth:
    if left is _Truth.TRUE or right is _Truth.TRUE:
        return _Truth.TRUE
    if left is _Truth.FALSE and right is _Truth.FALSE:
        return _Truth.FALSE
    return _Truth.UNKNOWN


def _not(state: _Truth) -> _Truth:
    if state is _Truth.UNKNOWN:
        return state
    return _Truth(state is _Truth.FALSE)


def _at_least_two(true_count: int, unknown_count: int) -> _Truth:
    if true_count >= 2:
        return _Truth.TRUE
    if true_count + unknown_count < 2:
        return _Truth.FALSE
    return _Truth.UNKNOWN


def _rule_states(values: tuple[_Truth, ...]) -> tuple[_Truth, _Truth, _Truth]:
    allergen, inhaled, skin, respiratory, circulatory, digestive = values
    symptoms = (skin, respiratory, circulatory, digestive)
    count = _at_least_two(symptoms.count(_Truth.TRUE), symptoms.count(_Truth.UNKNOWN))
    return (
        _and(_and(_not(allergen), skin), _or(respiratory, circulatory)),
        _and(allergen, count),
        _and(allergen, _or(_and(_not(inhaled), respiratory), circulatory)),
    )


def _tier2_coverage(
    values: tuple[_Truth, ...], states: tuple[_Truth, ...]
) -> _Truth:
    if _Truth.TRUE in states:
        return _Truth.TRUE
    if _Truth.UNKNOWN not in states:
        return _Truth.FALSE

    # An individually unknown rule can still cover every completion together
    # with another rule. The same missing allergen flag feeds all three rules.
    choices = [
        (_Truth.FALSE, _Truth.TRUE) if value is _Truth.UNKNOWN else (value,)
        for value in values
    ]
    if all(_Truth.TRUE in _rule_states(world) for world in product(*choices)):
        return _Truth.TRUE
    return _Truth.UNKNOWN


def _validate(patient: PatientInput) -> None:
    if not isinstance(patient, dict):
        raise TypeError("Đầu vào phải là dict.")
    if any(type(key) is not str or key not in PatientInput.__annotations__ for key in patient):
        raise ValueError("Đầu vào có khóa ngoài bảng quyết định.")

    age = patient.get("tuoi")
    if age is not None:
        if type(age) not in (int, float):
            raise TypeError("Tuổi phải là số.")
        if age < 0 or (type(age) is float and not isfinite(age)):
            raise ValueError("Tuổi phải hữu hạn và không âm.")

    for field, minimum in (("huyet_ap_tam_thu", 0), ("huyet_ap_tam_thu_nen", 1)):
        pressure = patient.get(field)
        if pressure is None:
            continue
        if type(pressure) is not int:
            raise TypeError(f"{field} phải là số nguyên.")
        if pressure < minimum:
            raise ValueError(f"{field} nằm ngoài miền hợp lệ.")

    for field in _BOOLEAN_FIELDS:
        value = patient.get(field)
        if value is not None and type(value) is not bool:
            raise TypeError(f"{field} phải là boolean.")


def _hypotension(age: float | None, pressure: int | None, baseline: int | None) -> _Truth:
    if age is None or pressure is None:
        return _Truth.UNKNOWN
    if age < 1:
        return _Truth(pressure < 70)
    if age < 11:
        # Trừ trước để giữ ranh giới khi tuổi lẻ rất sát ngưỡng.
        return _Truth(pressure - 70 < 2 * age)
    if pressure < 90:
        return _Truth.TRUE
    if age < 18:
        return _Truth.FALSE
    if baseline is None:
        return _Truth.UNKNOWN
    # So sánh chính xác ở biên giảm đúng 30%, kể cả với số nguyên lớn.
    return _Truth(10 * pressure < 7 * baseline)


def _classify_valid(patient: PatientInput) -> ClassificationResult:
    age = patient.get("tuoi")
    if age is None:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Chưa kết luận vì thiếu tuổi để chọn ngưỡng huyết áp.",
        }

    values = tuple(_Truth(patient.get(field)) for field in _BOOLEAN_FIELDS)
    states = _rule_states(values)
    coverage = _tier2_coverage(values, states)
    if coverage is _Truth.FALSE:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Các dữ kiện hiện có không khớp quy tắc phản vệ nào trong bảng quyết định.",
        }
    if coverage is _Truth.UNKNOWN:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Chưa đủ thông tin để xác định có thỏa quy tắc phản vệ hay không.",
        }

    pressure = patient.get("huyet_ap_tam_thu")
    baseline = patient.get("huyet_ap_tam_thu_nen")
    if _hypotension(age, pressure, baseline) is _Truth.TRUE:
        return {
            "muc_do": "SOC_PHAN_VE",
            "rule_id": "R-SOC",
            "ly_do": "Thỏa R-SOC vì đủ tiêu chí phản vệ và tụt huyết áp tâm thu theo tuổi.",
        }

    possible = [(rule, state) for rule, state in zip(_RULE_IDS, states) if state is not _Truth.FALSE]
    selected, selected_state = possible[0]
    if selected_state is _Truth.TRUE:
        reason = f"Thỏa {selected} theo dữ kiện hiện có."
    else:
        missing = ", ".join(
            label for label, value in zip(_BOOLEAN_FIELDS.values(), values)
            if value is _Truth.UNKNOWN
        )
        possible_codes = ", ".join(rule for rule, _ in possible)
        reason = (
            f"Mọi khả năng đều thỏa tiêu chí phản vệ qua ít nhất một trong các rule {possible_codes}. "
            f"{selected} là mã đại diện vì thiếu thông tin về "
            f"{missing}. Chưa xác nhận riêng {selected}."
        )
    if pressure is None:
        reason += " Chưa đánh giá được tiêu chí sốc vì thiếu huyết áp tâm thu hiện tại."
    elif age >= 18 and baseline is None:
        reason += " Chưa đánh giá được mức giảm tương đối vì thiếu huyết áp nền."
    return {"muc_do": "PHAN_VE", "rule_id": selected, "ly_do": reason}


def classify(patient: PatientInput) -> ClassificationResult:
    """Phân loại dữ liệu giả lập và hoàn tất audit trước khi trả kết quả."""
    with _audit_call() as user_uuid:
        validation_error = None
        try:
            _validate(patient)
        except (TypeError, ValueError) as error:
            validation_error = error
        if validation_error is not None:
            _write_record(user_uuid, "INVALID_INPUT")
            raise validation_error from None

        try:
            result = _classify_valid(patient)
        except Exception:
            # INT-013: lỗi nội bộ không thuộc hai trạng thái audit hiện hành.
            pass
        else:
            _write_record(user_uuid, "SUCCESS")
            return result
        raise RuntimeError("Không thể hoàn tất phân loại.") from None
