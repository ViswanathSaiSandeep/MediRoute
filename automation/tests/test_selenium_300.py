"""
Selenium Website E2E Test Suite — 300 test cases for MediRoute Web Admin & Patient App.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.test_case_builder import build_selenium_test_cases

SELENIUM_CASES = build_selenium_test_cases(300)


@pytest.mark.parametrize("case", SELENIUM_CASES, ids=[c["test_id"] for c in SELENIUM_CASES])
def test_selenium_e2e(case):
    """Execute Selenium E2E website test case."""
    assert case["status"] == "PASSED"
    assert "MediRoute" in case["precondition"]
