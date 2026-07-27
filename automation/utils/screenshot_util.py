"""
Screenshot utility – captures screenshots on test failure and on demand.
"""

import os
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SCREENSHOTS_DIR


def capture_screenshot(driver, name: str) -> str:
    """Capture a screenshot and return the file path."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        return filepath
    except Exception as e:
        print(f"[SCREENSHOT] Failed to capture: {e}")
        return ""


def capture_failure_screenshot(driver, test_name: str) -> str:
    """Capture a screenshot specifically for a test failure."""
    return capture_screenshot(driver, f"FAIL_{test_name}")


def capture_element_screenshot(driver, element, name: str) -> str:
    """Capture a screenshot of a specific element."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    filename = f"element_{safe_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        element.screenshot(filepath)
        return filepath
    except Exception:
        return capture_screenshot(driver, name)


def get_browser_console_logs(driver) -> list:
    """Get browser console logs."""
    try:
        return driver.get_log("browser")
    except Exception:
        return []


def get_performance_logs(driver) -> list:
    """Get performance logs."""
    try:
        return driver.get_log("performance")
    except Exception:
        return []
