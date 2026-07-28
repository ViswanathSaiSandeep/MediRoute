"""
Unit Tests — API (300 test cases)
Tests static assets, routes, HTTP methods, headers, and config against LIVE deployment.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.test_case_builder import build_unit_test_cases
from shared.test_executors import execute_unit_case

UNIT_CASES = build_unit_test_cases(300)


@pytest.mark.parametrize("case", UNIT_CASES, ids=[c["id"] for c in UNIT_CASES])
def test_unit_api(case):
    """Execute unit/API test case against live GitHub Pages deployment."""
    execute_unit_case(case)
