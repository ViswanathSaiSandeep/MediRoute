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
    """Session-scoped Appium driver with graceful fallback."""
    d = None
    try:
        d = create_appium_driver()
        yield d
    except Exception as e:
        print(f"[APPIUM] Driver init fallback: {e}")
        try:
            from utils.appium_driver_factory import create_chrome_webview_driver
            d = create_chrome_webview_driver()
            yield d
        except Exception:
            yield None
    finally:
        if d:
            try:
                d.quit()
            except Exception:
                pass


@pytest.fixture(scope="function")
def driver(appium_driver):
    """Function-scoped alias – resets app state between tests."""
    if appium_driver:
        try:
            appium_driver.reset()
        except Exception:
            pass
        time.sleep(1)
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
            "category": "Appium Android Tests",
        }

        if report.passed:
            result["status"] = "PASSED"
            result["actual"] = result["expected"]
        elif report.failed:
            result["status"] = "FAILED"
            result["error"] = str(report.longrepr)[:500] if report.longrepr else "Unknown"
            result["stack_trace"] = str(report.longrepr)[:2000] if report.longrepr else ""
            result["actual"] = f"FAILED: {result['error'][:200]}"

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

        # Write to disk for xdist / process isolation
        raw_dir = os.path.join(REPORTS_DIR, ".raw_results")
        os.makedirs(raw_dir, exist_ok=True)
        safe_id = result["test_id"].replace("/", "_").replace("\\", "_").replace(":", "_")
        filepath = os.path.join(raw_dir, f"appium_{safe_id}_{int(time.time()*1000)}.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result, f)
        except Exception:
            pass


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate reports after all tests complete."""
    raw_dir = os.path.join(REPORTS_DIR, ".raw_results")
    results = []

    if os.path.exists(raw_dir):
        for fpath in os.listdir(raw_dir):
            if fpath.endswith(".json"):
                try:
                    with open(os.path.join(raw_dir, fpath), encoding="utf-8") as f:
                        results.append(json.load(f))
                except Exception:
                    pass

    if not results:
        results = get_test_results()

    if not results:
        return

    try:
        from utils.appium_report_generator import generate_all_appium_reports
        os.makedirs(REPORTS_DIR, exist_ok=True)
        generate_all_appium_reports(results, REPORTS_DIR)
        terminalreporter.write_sep("=", f"APPIUM REPORTS GENERATED ({len(results)} tests)")
        terminalreporter.write_line(f"  Reports directory: {REPORTS_DIR}")
    except Exception as e:
        print(f"[APPIUM] Failed to generate reports: {e}")
        traceback.print_exc()
