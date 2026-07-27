"""
Explicit wait helpers for Selenium interactions.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import EXPLICIT_WAIT, FLUTTER_LOAD_TIMEOUT


def wait_for_element(driver, by, value, timeout=EXPLICIT_WAIT):
    """Wait for an element to be present in the DOM."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_for_element_visible(driver, by, value, timeout=EXPLICIT_WAIT):
    """Wait for an element to be visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def wait_for_element_clickable(driver, by, value, timeout=EXPLICIT_WAIT):
    """Wait for an element to be clickable."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def wait_for_text_present(driver, by, value, text, timeout=EXPLICIT_WAIT):
    """Wait for specific text to appear in an element."""
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((by, value), text)
    )


def wait_for_url_contains(driver, url_part, timeout=EXPLICIT_WAIT):
    """Wait for URL to contain a specific string."""
    return WebDriverWait(driver, timeout).until(
        EC.url_contains(url_part)
    )


def wait_for_page_load(driver, timeout=FLUTTER_LOAD_TIMEOUT):
    """Wait for the page to fully load (document.readyState === 'complete')."""
    return WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def wait_for_flutter_ready(driver, timeout=FLUTTER_LOAD_TIMEOUT):
    """Wait for Flutter web app to finish bootstrapping."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "return typeof _flutter !== 'undefined' || "
                "document.querySelector('flt-glass-pane') !== null || "
                "document.querySelector('flutter-view') !== null || "
                "document.querySelector('canvas') !== null || "
                "document.readyState === 'complete'"
            )
        )
        return True
    except TimeoutException:
        return False


def wait_for_element_disappear(driver, by, value, timeout=EXPLICIT_WAIT):
    """Wait for an element to disappear from the DOM."""
    return WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((by, value))
    )


def wait_for_any_element(driver, locators, timeout=EXPLICIT_WAIT):
    """Wait for any one of multiple elements to be present."""
    def any_present(d):
        for by, value in locators:
            try:
                el = d.find_element(by, value)
                if el:
                    return el
            except Exception:
                continue
        return False

    return WebDriverWait(driver, timeout).until(any_present)


def is_element_present(driver, by, value, timeout=3):
    """Check if an element is present (non-blocking)."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False
