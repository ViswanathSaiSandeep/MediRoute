"""
Validation Tests (300 test cases)
Input validation, content validation, route validation against LIVE deployment.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.test_case_builder import build_validation_test_cases
from shared.test_executors import execute_validation_case

VALIDATION_CASES = build_validation_test_cases(300)


@pytest.mark.parametrize("case", VALIDATION_CASES, ids=[c["id"] for c in VALIDATION_CASES])
def test_validation(case):
    """Execute validation test case."""
    execute_validation_case(case)
