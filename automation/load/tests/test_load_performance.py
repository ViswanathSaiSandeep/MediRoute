"""
Load Testing — Performance (300 test cases)
Concurrent and sequential load tests against LIVE GitHub Pages deployment.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.test_case_builder import build_load_test_cases
from shared.test_executors import execute_load_case

LOAD_CASES = build_load_test_cases(300)


@pytest.mark.parametrize("case", LOAD_CASES, ids=[c["id"] for c in LOAD_CASES])
def test_load_performance(case):
    """Execute load/performance test against live deployment."""
    execute_load_case(case)
