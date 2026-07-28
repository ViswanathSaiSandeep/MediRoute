"""
Shared pytest hooks for HTTP-based test categories.
Import and call register_category_hooks() from each category conftest.
"""

import os
import sys
import traceback
import time

_test_results = []


def get_category_results():
    return _test_results


def register_category_hooks(category_name: str, reports_dir: str):
    """Register pytest hooks for a test category.
    Returns (makereport_hook, terminal_summary_hook) for the caller to install.
    """

    def makereport_hook(item, call):
        """Hook wrapper for pytest_runtest_makereport."""
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            case = getattr(item, "callspec", None)
            case_params = case.params.get("case", {}) if case else {}

            result = {
                "test_id": case_params.get("id", item.nodeid.split("::")[-1]),
                "module": case_params.get("module", category_name),
                "test_name": case_params.get("name", item.name),
                "priority": case_params.get("priority", "Medium"),
                "precondition": case_params.get("precondition", "Deployment live"),
                "expected": case_params.get("expected", "Test passes"),
                "actual": "",
                "status": "",
                "duration": report.duration,
                "error": "",
                "stack_trace": "",
                "category": category_name,
            }

            if report.passed:
                result["status"] = "PASSED"
                result["actual"] = result["expected"]
            elif report.failed:
                result["status"] = "FAILED"
                result["error"] = str(report.longrepr)[:500] if report.longrepr else "Unknown"
                result["stack_trace"] = str(report.longrepr)[:2000] if report.longrepr else ""
                result["actual"] = f"FAILED: {result['error'][:200]}"
            elif report.skipped:
                result["status"] = "SKIPPED"
                result["actual"] = "SKIPPED"

            _test_results.append(result)

    def terminal_summary_hook(terminalreporter, exitstatus, config):
        """Hook for pytest_terminal_summary — generates category reports."""
        results = list(_test_results)  # snapshot
        if not results:
            return
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
            from shared.category_report import generate_category_reports
            os.makedirs(reports_dir, exist_ok=True)
            generate_category_reports(results, category_name, reports_dir)
            terminalreporter.write_sep("=", f"{category_name.upper()} REPORTS GENERATED")
            terminalreporter.write_line(f"  Reports directory: {reports_dir}")
        except Exception as e:
            print(f"[{category_name}] Report generation failed: {e}")
            traceback.print_exc()

    return makereport_hook, terminal_summary_hook
