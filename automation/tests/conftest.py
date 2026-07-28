"""
Pytest conftest.py – shared fixtures for the MediRoute E2E test suite.
"""

import pytest
import os
import sys
import time
import json
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import create_driver
from utils.screenshot_util import capture_failure_screenshot, get_browser_console_logs
from utils.logger_util import get_logger
from config.settings import BASE_URL, SCREENSHOTS_DIR, REPORTS_DIR

logger = get_logger("conftest")

# Global results collector
_test_results = []


def get_test_results():
    return _test_results


@pytest.fixture(scope="session")
def base_url():
    """Provide the configured BASE_URL."""
    return BASE_URL


@pytest.fixture(scope="function")
def driver():
    """Create a fresh WebDriver for each test."""
    d = None
    try:
        d = create_driver()
        yield d
    finally:
        if d:
            try:
                d.quit()
            except Exception:
                pass


@pytest.fixture(scope="session")
def shared_driver():
    """Session-scoped driver for tests that can share state."""
    d = None
    try:
        d = create_driver()
        yield d
    finally:
        if d:
            try:
                d.quit()
            except Exception:
                pass


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
            "precondition": getattr(item, "_precondition", "Application loaded"),
            "expected": getattr(item, "_expected", "Test passes"),
            "actual": "",
            "status": "",
            "duration": report.duration,
            "error": "",
            "stack_trace": "",
            "screenshot": "",
            "console_logs": [],
        }

        if report.passed:
            result["status"] = "PASSED"
            result["actual"] = result["expected"]
        elif report.failed:
            result["status"] = "FAILED"
            result["error"] = str(report.longrepr)[:500] if report.longrepr else "Unknown error"
            result["stack_trace"] = str(report.longrepr)[:2000] if report.longrepr else ""
            result["actual"] = f"FAILED: {result['error'][:200]}"

            # Capture screenshot on failure
            driver = item.funcargs.get("driver") or item.funcargs.get("shared_driver")
            if driver:
                try:
                    result["screenshot"] = capture_failure_screenshot(driver, item.name)
                    result["console_logs"] = get_browser_console_logs(driver)
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
        from utils.report_generator import generate_html_report, generate_dashboard
        from utils.excel_generator import generate_all_excel_reports
        from utils.summary_generator import generate_summary_md, generate_json_results

        os.makedirs(REPORTS_DIR, exist_ok=True)

        summary = {
            "total": len(results),
            "passed": len([r for r in results if r["status"] == "PASSED"]),
            "failed": len([r for r in results if r["status"] == "FAILED"]),
            "skipped": len([r for r in results if r["status"] == "SKIPPED"]),
        }

        generate_html_report(results, summary)
        generate_dashboard(results, summary)
        generate_all_excel_reports(results)
        generate_summary_md(results)
        generate_json_results(results, summary)

        # Category-specific report for CI artifacts
        try:
            from shared.category_report import generate_category_reports
            for r in results:
                r.setdefault("category", "Selenium Website Tests")
            generate_category_reports(results, "Selenium Website Tests", REPORTS_DIR)
        except Exception as cat_err:
            logger.warning(f"Category report generation: {cat_err}")

        logger.info(f"Reports generated in {REPORTS_DIR}")
        terminalreporter.write_sep("=", "REPORTS GENERATED SUCCESSFULLY")
        terminalreporter.write_line(f"  Reports directory: {REPORTS_DIR}")
    except Exception as e:
        logger.error(f"Failed to generate reports: {e}")
        traceback.print_exc()
