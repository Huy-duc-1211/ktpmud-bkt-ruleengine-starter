import math
import re
from collections import defaultdict
from copy import deepcopy
from itertools import product

import pytest

from run_case import DEFAULT_CSV, FIXTURES_DIR, load_patient, read_cases, read_json
from rule_engine.classifier import (
    _BOOLEAN_FIELDS,
    _RULE_IDS,
    _Truth,
    _and,
    _at_least_two,
    _hypotension,
    _not,
    _or,
    _rule_states,
    _tier2_coverage,
    classify,
)


_PUBLIC_CASES = read_cases(DEFAULT_CSV)
_INTERNAL_CASES = read_cases(FIXTURES_DIR / "INTERNAL_STATE_CASES.csv")

_MISSING = r"(?:thiếu|chưa có|không có)"
_UNCERTAIN = (
    r"(?:(?:thiếu|chưa đủ|không đủ) (?:thông tin|dữ liệu|dữ kiện)|"
    r"(?:chưa|không) (?:thể )?(?:kết luận|xác định|đánh giá)(?: được)?)"
)
_NO_RULE = r"\bkhông (?:khớp|thỏa|đáp ứng)\b"
_REPRESENTATIVE = r"\b(?:mã đại diện|canonical)\b"
_NOT_VERIFIED = r"\b(?:chưa|không)(?: thể)? xác nhận (?:riêng|độc lập)\b"
_CURRENT_BP = r"(?:hatt|huyết áp(?: tâm thu)?) hiện tại"
_BASELINE_BP = r"(?:hatt|huyết áp(?: tâm thu)?) nền"

_MISSING_AGE = rf"\b(?:{_MISSING}(?: thông tin về)? tuổi|tuổi(?: của bệnh nhân)? {_MISSING})\b"
_MISSING_CURRENT_BP = rf"\b(?:{_MISSING}(?: số đo)? {_CURRENT_BP}|{_CURRENT_BP} {_MISSING})\b"
_MISSING_BASELINE_BP = rf"\b(?:{_MISSING}(?: số đo)? {_BASELINE_BP}|{_BASELINE_BP} {_MISSING})\b"

_REASON_REQUIREMENTS = {
    "thiếu tuổi": _MISSING_AGE,
    "thiếu huyết áp": _MISSING_CURRENT_BP,
    "thiếu huyết áp nền": _MISSING_BASELINE_BP,
    "chưa đánh giá được tiêu chí sốc": rf"{_UNCERTAIN}[^.!?;]*\bsốc\b",
    "chưa đánh giá được mức giảm tương đối": rf"{_UNCERTAIN}[^.!?;]*\bgiảm tương đối\b",
}


def _assert_uncertain_reason(reason):
    assert re.search(_UNCERTAIN, reason) and "phản vệ" in reason
    # Kiểm mệnh đề độc lập để phân biệt "chưa thể kết luận không có phản vệ"
    # với một kết luận bị chèn sau phần nêu thiếu thông tin.
    for clause in re.split(r"[.!?,;]|\b(?:nhưng|tuy nhiên|dù vậy|vì vậy|do đó)\b", reason):
        assert not re.match(
            r"\s*(?:(?:người bệnh|bệnh nhân|trường hợp này) )?"
            r"(?:(?:chắc chắn|đã xác định(?: là)?|(?:đã )?kết luận(?: là)?|có thể) )*"
            r"(?:không (?:có|bị) phản vệ|đã loại trừ phản vệ|loại trừ phản vệ|không khớp|có phản vệ)\b",
            clause,
        ), clause


def _assert_reason(result, patient, expected):
    assert isinstance(result["ly_do"], str) and result["ly_do"].strip()
    reason = " ".join(result["ly_do"].split()).casefold()
    rule = (result["rule_id"] or "").casefold()
    level = result["muc_do"]
    assertions = expected.get("explanation_assertions", {})
    kind = assertions.get("attribution_kind")
    assert not re.search(r"\b\d+(?:[.,]\d+)?\s*mmhg\b", reason)
    assert not re.search(
        r"\b(?:dùng|uống|tiêm|truyền|kê|sử dụng|điều trị bằng)\s+(?:thêm\s+)?"
        r"(?:thuốc\b|adrenalin\w*|epinephrin\w*)",
        reason,
    )

    if level == "THEO_DOI":
        if patient.get("tuoi") is None:
            assert re.search(_MISSING_AGE, reason) and re.search(_UNCERTAIN, reason)
        elif kind == "MIXED" or (kind != "NO_RULE" and re.search(_UNCERTAIN, reason)):
            _assert_uncertain_reason(reason)
        else:
            assert re.search(_NO_RULE, reason) and "phản vệ" in reason
    elif level == "SOC_PHAN_VE":
        assert rule in reason and "phản vệ" in reason
        assert re.search(r"\b(?:tụt|giảm|hạ|thấp)\b", reason)
        assert re.search(r"\b(?:hatt|huyết áp tâm thu)\b", reason)
    else:
        assert rule in reason
        representative = re.search(_REPRESENTATIVE, reason)
        if kind == "DIRECT":
            assert not representative
        if kind == "CANONICAL" or representative:
            assert representative and re.search(_NOT_VERIFIED, reason)
            assert re.search(_MISSING, reason)
            assert any(
                label in reason for field, label in _BOOLEAN_FIELDS.items() if patient.get(field) is None
            )
            assert not re.search(
                rf"\b{re.escape(rule)} (?:đã (?:được )?xác nhận|chắc chắn (?:đúng|thỏa))\b", reason
            )
        else:
            assert re.search(r"\b(?:thỏa|khớp|đáp ứng)\b", reason)
            assert not re.search(rf"{_NO_RULE} (?:quy tắc )?{re.escape(rule)}\b", reason)

        if patient.get("huyet_ap_tam_thu") is None:
            assert re.search(_MISSING_CURRENT_BP, reason)
            assert re.search(_REASON_REQUIREMENTS["chưa đánh giá được tiêu chí sốc"], reason)
            assert not re.search(rf"{_CURRENT_BP} đã (?:rõ|biết|đo được)", reason)
        elif patient["tuoi"] >= 18 and patient.get("huyet_ap_tam_thu_nen") is None:
            assert re.search(_MISSING_BASELINE_BP, reason)
            assert re.search(_REASON_REQUIREMENTS["chưa đánh giá được mức giảm tương đối"], reason)
            assert not re.search(rf"{_BASELINE_BP} đã (?:rõ|biết|đo được)", reason)

    for phrase in expected.get("reason_must_mention", []):
        assert re.search(_REASON_REQUIREMENTS.get(phrase, re.escape(phrase)), reason), phrase
    for pattern in assertions.get("required_patterns_all", []):
        assert re.search(pattern, reason, re.IGNORECASE), pattern
    for pattern in assertions.get("forbidden_patterns_any", []):
        assert not re.search(pattern, reason, re.IGNORECASE), pattern


@pytest.mark.parametrize("case", _PUBLIC_CASES, ids=[case["Test ID"] for case in _PUBLIC_CASES])
def test_designed_case(case, audit_records, capsys, caplog):
    patient = load_patient(case)
    expected = read_json(case["Expected"])
    if case["Fixture encoding"] == "fixture_ref":
        age = patient["tuoi"]
        assert type(age) is float
        matches = {
            "INV-005": math.isnan(age),
            "INV-006": math.isinf(age) and age > 0,
            "INV-007": math.isinf(age) and age < 0,
        }
        assert matches[case["Test ID"]]
    if "exception_class" in expected:
        error_type = {"TypeError": TypeError, "ValueError": ValueError}[expected["exception_class"]]
        with pytest.raises(error_type) as caught:
            classify(patient)
        assert type(caught.value) is error_type
        assert caught.value.__context__ is None
        audit_records("INVALID_INPUT")
    else:
        original = deepcopy(patient)
        result = classify(patient)
        assert set(result) == {"muc_do", "rule_id", "ly_do"}
        assert result["muc_do"] == expected["muc_do"]
        assert result["rule_id"] == expected["rule_id"]
        _assert_reason(result, patient, expected)
        assert patient == original
        audit_records("SUCCESS")
    captured = capsys.readouterr()
    assert not captured.out and not captured.err and not caplog.records


@pytest.mark.parametrize(("case_id", "bad_reason"), [
    ("MISS-012", "Chưa đủ thông tin để xác định, nhưng chắc chắn không có phản vệ."),
    ("MISS-012", "Chưa đủ thông tin để xác định. Đã loại trừ phản vệ."),
    ("RULE-002", "Thỏa R01-PV theo dữ kiện hiện có. Hãy dùng thuốc ngay."),
    ("PEND-003", "Thỏa R01-PV theo dữ kiện hiện có. Huyết áp tâm thu hiện tại đã rõ."),
    ("MISS-009", "Mọi khả năng đều thỏa tiêu chí phản vệ qua ít nhất một trong các rule "
     "R01-PV, R02-PV. R01-PV là mã đại diện vì thiếu thông tin. Chưa xác nhận riêng R01-PV."),
    ("MISS-009", "Mọi khả năng đều thỏa tiêu chí phản vệ qua ít nhất một trong các rule "
     "R01-PV, R02-PV. R01-PV là mã đại diện vì thiếu thông tin về dị nguyên nghi ngờ. "
     "R01-PV đã được xác nhận chắc chắn."),
], ids=[
    "mixed-contradiction", "mixed-exclusion", "treatment-advice", "missing-pressure",
    "canonical-no-field", "canonical-overclaim",
])
def test_ly_do_rejects_counterexamples(case_id, bad_reason):
    case = next(case for case in _PUBLIC_CASES if case["Test ID"] == case_id)
    patient = load_patient(case)
    expected = read_json(case["Expected"])
    result = classify(patient)
    _assert_reason(result, patient, expected)

    result["ly_do"] = bad_reason
    with pytest.raises(AssertionError):
        _assert_reason(result, patient, expected)


@pytest.mark.parametrize(("case_id", "paraphrase"), [
    ("PEND-002", "Chưa thể xác định mức phân loại vì chưa có thông tin về tuổi."),
    ("MISS-012", "Chưa thể kết luận không có phản vệ vì chưa đủ dữ kiện."),
    ("MISS-012", "Thiếu dữ kiện để đưa ra kết luận về phản vệ."),
    ("RULE-020", "Dữ kiện hiện tại không đáp ứng quy tắc phản vệ nào."),
    ("RULE-002", "Dữ liệu đầu vào đáp ứng quy tắc R01-PV."),
    ("MISS-009", "Mọi khả năng đều đáp ứng tiêu chí phản vệ qua R01-PV hoặc R02-PV. "
     "Vì thiếu thông tin về dị nguyên nghi ngờ, dùng R01-PV làm mã đại diện. "
     "Chưa thể xác nhận độc lập R01-PV."),
    ("D13E-003", "R-SOC áp dụng khi đủ tiêu chí phản vệ và huyết áp tâm thu thấp theo tuổi."),
    ("PEND-003", "Do chưa có HATT hiện tại, chưa thể đánh giá tiêu chí sốc. "
     "Các dữ kiện đáp ứng R01-PV."),
    ("PEND-005", "Thỏa R02-PV. HATT nền chưa có nên chưa thể đánh giá mức giảm tương đối."),
], ids=[
    "missing-age", "mixed-no-conclusion", "mixed-insufficient-data", "no-rule", "direct", "canonical",
    "shock", "missing-current-bp", "missing-baseline-bp",
])
def test_ly_do_accepts_equivalent_wording(case_id, paraphrase):
    case = next(case for case in _PUBLIC_CASES if case["Test ID"] == case_id)
    patient = load_patient(case)
    expected = read_json(case["Expected"])
    result = classify(patient)
    result["ly_do"] = paraphrase
    _assert_reason(result, patient, expected)


_CASES_WITH_STATES = [
    case for case in _PUBLIC_CASES
    if case["Internal assertions"] and "states" in read_json(case["Internal assertions"])
]


@pytest.mark.parametrize(
    "case", _CASES_WITH_STATES, ids=[case["Test ID"] for case in _CASES_WITH_STATES]
)
def test_designed_internal_states(case):
    patient = load_patient(case)
    internal = read_json(case["Internal assertions"])
    values = tuple(_Truth(patient.get(field)) for field in _BOOLEAN_FIELDS)
    states = _rule_states(values)
    coverage = _tier2_coverage(values, states)
    low = _hypotension(
        patient.get("tuoi"), patient.get("huyet_ap_tam_thu"), patient.get("huyet_ap_tam_thu_nen")
    )
    actual = {
        **dict(zip(("R01", "R02", "R03"), states)),
        "HYPOTENSION": low,
        "HYPOTENSION_EVIDENCE": _Truth(low is _Truth.TRUE),
        "TIER2_COVERAGE": coverage,
        "TIER1_MATCH": _and(coverage, low),
    }
    for name, expected in internal["states"].items():
        assert actual[name] is _Truth[expected], name
    count = internal.get("r02_count")
    if count:
        symptoms = values[2:]
        known = symptoms.count(_Truth.TRUE)
        unknown = symptoms.count(_Truth.UNKNOWN)
        assert (known, unknown) == (count["T"], count["U"])
        assert _at_least_two(known, unknown) is _Truth[count["state"]]
    selection = internal.get("selection")
    if selection:
        assert [rule for rule, state in zip(_RULE_IDS, states) if state is _Truth.TRUE] == (
            selection["definite_rules"]
        )
        assert [rule for rule, state in zip(_RULE_IDS, states) if state is not _Truth.FALSE] == (
            selection["possible_rules"]
        )
        assert (coverage is _Truth.TRUE) == selection["all_completions_have_anaphylaxis"]
        assert (coverage is not _Truth.FALSE) == selection["any_completion_has_anaphylaxis"]
        if "completion_count" in selection:
            assert 2 ** values.count(_Truth.UNKNOWN) == selection["completion_count"]


@pytest.mark.parametrize("case", _INTERNAL_CASES, ids=[case["Test ID"] for case in _INTERNAL_CASES])
def test_kleene_tables(case):
    operation = case["Operation"]
    binary = {"AND": _and, "OR": _or}
    if operation in binary:
        actual = binary[operation](_Truth[case["Left"]], _Truth[case["Right"]])
    elif operation == "NOT":
        actual = _not(_Truth[case["Left"]])
    else:
        actual = _at_least_two(int(case["T"]), int(case["U"]))
        if operation == "R02_AND_ALLERGEN":
            actual = _and(actual, _Truth[case["Allergen state"]])
        else:
            assert operation == "R02_COUNT"
    assert actual is _Truth[case["Expected enum"]]


def _full_input_rules(allergen, inhaled, skin, respiratory, circulatory, digestive):
    # Independent oracle from the decision table on complete inputs.
    matches = set()
    if not allergen and skin and (respiratory or circulatory):
        matches.add("R01-PV")
    if allergen and sum((skin, respiratory, circulatory, digestive)) >= 2:
        matches.add("R02-PV")
    if allergen and ((not inhaled and respiratory) or circulatory):
        matches.add("R03-PV")
    return matches


def test_all_729_boolean_patterns():
    rule_order = ("R01-PV", "R02-PV", "R03-PV")
    assert tuple(_BOOLEAN_FIELDS) == (
        "co_di_nguyen_nghi_ngo",
        "di_nguyen_qua_duong_hit",
        "co_ton_thuong_da_niem_mac",
        "co_trieu_chung_ho_hap",
        "co_trieu_chung_tuan_hoan",
        "co_trieu_chung_tieu_hoa_nang",
    )
    for pattern in product((False, True, None), repeat=6):
        choices = [(True, False) if value is None else (value,) for value in pattern]
        worlds = [_full_input_rules(*world) for world in product(*choices)]
        definite = set.intersection(*worlds)
        possible = set.union(*worlds)
        patient = dict(zip(_BOOLEAN_FIELDS, pattern), tuoi=15, huyet_ap_tam_thu=110)
        result = classify(patient)
        assert result == classify(dict(reversed(list(patient.items())))), pattern
        if all(worlds):
            rule_id = next(rule for rule in rule_order if rule in possible)
            assert (result["muc_do"], result["rule_id"]) == ("PHAN_VE", rule_id), pattern
            kind = "DIRECT" if rule_id in definite else "CANONICAL"
        else:
            assert (result["muc_do"], result["rule_id"]) == ("THEO_DOI", None), pattern
            kind = "MIXED" if possible else "NO_RULE"
        _assert_reason(result, patient, {"explanation_assertions": {"attribution_kind": kind}})
        states = _rule_states(tuple(map(_Truth, pattern)))
        assert {rule for rule, state in zip(rule_order, states) if state is _Truth.TRUE} == definite
        assert {rule for rule, state in zip(rule_order, states) if state is not _Truth.FALSE} == possible


_EQUIVALENT_CASES = defaultdict(list)
for _case in _PUBLIC_CASES:
    if _case["Equivalence group"]:
        _EQUIVALENT_CASES[_case["Equivalence group"]].append(_case)


@pytest.mark.parametrize("group", _EQUIVALENT_CASES)
def test_missing_and_null_are_equivalent(group):
    first, second = (classify(load_patient(case)) for case in _EQUIVALENT_CASES[group])
    assert (first["muc_do"], first["rule_id"]) == (second["muc_do"], second["rule_id"])


@pytest.mark.parametrize(("case_id", "missing_field"), [
    ("MISS-009", "dị nguyên nghi ngờ"),
    ("MISS-013", "hô hấp"),
    ("MISS-014", r"\bda\b|niêm mạc"),
])
def test_canonical_names_the_missing_field_and_limits_attribution(case_id, missing_field):
    case = next(case for case in _PUBLIC_CASES if case["Test ID"] == case_id)
    patient = load_patient(case)
    result = classify(patient)
    _assert_reason(result, patient, read_json(case["Expected"]))
    assert re.search(missing_field, result["ly_do"], re.IGNORECASE)


def test_unbounded_integer_pressures_keep_exact_30_percent_boundary():
    patient = {
        "tuoi": 10**400,
        "huyet_ap_tam_thu_nen": 10**401,
        "huyet_ap_tam_thu": 7 * 10**400,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    }
    assert classify(patient)["rule_id"] == "R01-PV"
    patient["huyet_ap_tam_thu"] -= 1
    assert classify(patient)["rule_id"] == "R-SOC"


def test_fractional_age_just_above_pressure_boundary():
    assert _hypotension(5, 80, None) is _Truth.FALSE
    assert _hypotension(math.nextafter(5, math.inf), 80, None) is _Truth.TRUE
