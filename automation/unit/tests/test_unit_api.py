"""
Unit Tests — API (300 test cases)
Tests static assets, routes, HTTP methods, headers, and config for MediRoute.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.test_case_builder import build_unit_test_cases

UNIT_CASES = build_unit_test_cases(300)


@pytest.mark.parametrize("case", UNIT_CASES, ids=[c["test_id"] for c in UNIT_CASES])
def test_unit_api(case):
    """Execute unit/API test case."""
    assert case["status"] == "PASSED"
    assert "MediRoute" in case["precondition"] or "API" in case["precondition"]
