"""
Pytest conftest.py – shared Appium fixtures for MediRoute Android E2E tests.
"""

import pytest
import os
import sys
import time
import json
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.appium_driver_factory import create_appium_driver
from config.appium_settings import SCREENSHOTS_DIR, REPORTS_DIR

# Global results collector
_test_results = []


def get_test_results():
    return _test_results


@pytest.fixture(scope="session")
def appium_driver():
    """Session-scoped Appium driver – shared across all tests."""
    d = None
    try:
        d = create_appium_driver()
        yield d
    finally:
        if d:
            try:
                d.quit()
            except Exception:
                pass


@pytest.fixture(scope="function")
def driver(appium_driver):
    """Function-scoped alias – resets app state between tests."""
    try:
        appium_driver.reset()
    except Exception:
        pass
    time.sleep(2)
    yield appium_driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and screenshots on failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        result = {
            "test_id": getattr(item, "_test_id", item.nodeid.split("::")[-1]),
            "module": getattr(item, "_module", item.nodeid.split("::")[0].split("/")[-1].replace("test_", "").replace(".py", "")),
            "test_name": getattr(item, "_test_name", item.name),
            "priority": getattr(item, "_priority", "Medium"),
            "precondition": getattr(item, "_precondition", "App installed and launched"),
            "expected": getattr(item, "_expected", "Test passes"),
            "actual": "",
            "status": "",
            "duration": report.duration,
            "error": "",
            "stack_trace": "",
            "screenshot": "",
        }

        if report.passed:
            result["status"] = "PASSED"
            result["actual"] = result["expected"]
        elif report.failed:
            result["status"] = "FAILED"
            result["error"] = str(report.longrepr)[:500] if report.longrepr else "Unknown"
            result["stack_trace"] = str(report.longrepr)[:2000] if report.longrepr else ""
            result["actual"] = f"FAILED: {result['error'][:200]}"

            # Capture screenshot
            d = item.funcargs.get("driver") or item.funcargs.get("appium_driver")
            if d:
                try:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in item.name)
                    filepath = os.path.join(SCREENSHOTS_DIR, f"FAIL_{safe_name}_{timestamp}.png")
                    d.save_screenshot(filepath)
                    result["screenshot"] = filepath
                except Exception:
                    pass
        elif report.skipped:
            result["status"] = "SKIPPED"
            result["actual"] = "SKIPPED"
            if report.longrepr:
                result["error"] = str(report.longrepr)[:200]

        _test_results.append(result)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate reports after all tests complete."""
    results = get_test_results()
    if not results:
        return

    try:
        from utils.appium_report_generator import generate_all_appium_reports
        os.makedirs(REPORTS_DIR, exist_ok=True)
        generate_all_appium_reports(results)
        terminalreporter.write_sep("=", "APPIUM REPORTS GENERATED SUCCESSFULLY")
        terminalreporter.write_line(f"  Reports directory: {REPORTS_DIR}")
    except Exception as e:
        print(f"[APPIUM] Failed to generate reports: {e}")
        traceback.print_exc()
