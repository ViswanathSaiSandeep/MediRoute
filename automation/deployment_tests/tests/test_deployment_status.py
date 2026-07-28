"""
Deployment Status Tests (300 test cases)
Verifies live GitHub Pages deployment availability, assets, and stability.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.test_case_builder import build_deployment_test_cases
from shared.test_executors import execute_deployment_case

DEPLOYMENT_CASES = build_deployment_test_cases(300)


@pytest.mark.parametrize("case", DEPLOYMENT_CASES, ids=[c["id"] for c in DEPLOYMENT_CASES])
def test_deployment_status(case):
    """Execute deployment status test against live deployment."""
    execute_deployment_case(case)
