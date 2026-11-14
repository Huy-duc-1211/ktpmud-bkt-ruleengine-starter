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
        reason = result["ly_do"]
        assert isinstance(reason, str) and reason.strip()
        assert result["rule_id"] is None or result["rule_id"] in reason
        assert not re.search(r"\b\d+(?:[.,]\d+)?\s*mmHg\b", reason, re.IGNORECASE)
        for phrase in expected.get("reason_must_mention", []):
            assert phrase in reason.casefold()
        assertions = expected.get("explanation_assertions", {})
        for pattern in assertions.get("required_patterns_all", []):
            assert re.search(pattern, reason), pattern
        for pattern in assertions.get("forbidden_patterns_any", []):
            assert not re.search(pattern, reason), pattern
        assert patient == original
        audit_records("SUCCESS")
    captured = capsys.readouterr()
    assert not captured.out and not captured.err and not caplog.records


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
            assert ("mã đại diện" in result["ly_do"]) == (rule_id not in definite), pattern
        else:
            assert (result["muc_do"], result["rule_id"]) == ("THEO_DOI", None), pattern
            assert ("Chưa đủ thông tin" in result["ly_do"]) == bool(possible), pattern
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


@pytest.mark.parametrize(("case_id", "explanation"), [
    ("MISS-009", "R01-PV là mã đại diện vì thiếu thông tin về dị nguyên nghi ngờ. "
     "Chưa xác nhận riêng R01-PV."),
    ("MISS-013", "R02-PV là mã đại diện vì thiếu thông tin về triệu chứng hô hấp. "
     "Chưa xác nhận riêng R02-PV."),
    ("MISS-014", "R02-PV là mã đại diện vì thiếu thông tin về tổn thương da hoặc niêm mạc. "
     "Chưa xác nhận riêng R02-PV."),
])
def test_canonical_names_the_missing_field_and_limits_attribution(case_id, explanation):
    case = next(case for case in _PUBLIC_CASES if case["Test ID"] == case_id)
    assert classify(load_patient(case))["ly_do"].endswith(explanation)


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
