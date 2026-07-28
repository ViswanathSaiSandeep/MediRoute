"""Deployment status test category conftest."""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

from shared.category_conftest import register_category_hooks

_hook_makereport, _hook_summary = register_category_hooks("Deployment Status", REPORTS_DIR)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    yield from _hook_makereport(item, call)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    _hook_summary(terminalreporter, exitstatus, config)
