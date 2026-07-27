"""
Base Page Object – all page objects inherit from this.
Provides common methods for Flutter web app interaction.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    StaleElementReferenceException, ElementNotInteractableException,
)
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import BASE_URL, EXPLICIT_WAIT, FLUTTER_LOAD_TIMEOUT
from utils.screenshot_util import capture_screenshot
from utils.logger_util import get_logger


class BasePage:
    """Base class for all Page Objects in the MediRoute automation framework."""

    def __init__(self, driver):
        self.driver = driver
        self.base_url = BASE_URL
        self.logger = get_logger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    # ── Navigation ────────────────────────────────────────────────────────
    def navigate_to(self, path: str = ""):
        """Navigate to a path relative to BASE_URL."""
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        self.wait_for_page_ready()

    def navigate_to_route(self, route_name: str):
        """Navigate to a named route using the ROUTES config."""
        from config.settings import ROUTES
        path = ROUTES.get(route_name, "/")
        self.navigate_to(f"#{path}" if not path.startswith("#") else path)

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get the page title."""
        return self.driver.title

    def go_back(self):
        """Navigate back in browser history."""
        self.driver.back()

    def refresh(self):
        """Refresh the current page."""
        self.driver.refresh()
        self.wait_for_page_ready()

    # ── Wait Methods ──────────────────────────────────────────────────────
    def wait_for_page_ready(self, timeout=FLUTTER_LOAD_TIMEOUT):
        """Wait for Flutter web app to fully load."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Give Flutter extra time to bootstrap
            time.sleep(2)
        except TimeoutException:
            self.logger.warning("Page load timeout reached")

    def wait_for_flutter(self, timeout=FLUTTER_LOAD_TIMEOUT):
        """Wait specifically for Flutter engine initialization."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script(
                    "return document.querySelector('flutter-view') !== null || "
                    "document.querySelector('flt-glass-pane') !== null || "
                    "document.querySelector('canvas') !== null"
                )
            )
            return True
        except TimeoutException:
            self.logger.warning("Flutter engine did not initialize in time")
            return False

    # ── Element Finders ───────────────────────────────────────────────────
    def find_element(self, by, value, timeout=EXPLICIT_WAIT):
        """Find an element with explicit wait."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(by, value)
            )
        except TimeoutException:
            self.logger.error(f"Element not found: {by}={value}")
            return None

    def find_elements(self, by, value, timeout=EXPLICIT_WAIT):
        """Find multiple elements."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(by, value)) > 0
            )
            return self.driver.find_elements(by, value)
        except TimeoutException:
            return []

    def find_by_text(self, text, timeout=EXPLICIT_WAIT):
        """Find element by its visible text content."""
        try:
            return self.find_element(
                By.XPATH,
                f"//*[contains(text(), '{text}')]",
                timeout
            )
        except Exception:
            return None

    def find_by_semantic_label(self, label, timeout=EXPLICIT_WAIT):
        """Find Flutter element by its semantic/aria label."""
        try:
            return self.find_element(
                By.CSS_SELECTOR,
                f'[aria-label="{label}"], [flt-semantics-identifier="{label}"]',
                timeout
            )
        except Exception:
            return None

    def find_by_role(self, role, timeout=EXPLICIT_WAIT):
        """Find element by ARIA role."""
        return self.find_elements(
            By.CSS_SELECTOR,
            f'[role="{role}"]',
            timeout
        )

    # ── Element Interaction ───────────────────────────────────────────────
    def click_element(self, by, value, timeout=EXPLICIT_WAIT):
        """Click an element with retry on stale reference."""
        for attempt in range(3):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    lambda d: d.find_element(by, value)
                )
                element.click()
                return True
            except (StaleElementReferenceException, ElementNotInteractableException):
                time.sleep(1)
        return False

    def click_text(self, text):
        """Click element containing specific text."""
        el = self.find_by_text(text)
        if el:
            try:
                el.click()
                return True
            except Exception:
                self.driver.execute_script("arguments[0].click();", el)
                return True
        return False

    def type_text(self, by, value, text, clear_first=True):
        """Type text into an input element."""
        element = self.find_element(by, value)
        if element:
            if clear_first:
                element.clear()
            element.send_keys(text)
            return True
        return False

    def get_element_text(self, by, value, timeout=EXPLICIT_WAIT):
        """Get text content of an element."""
        element = self.find_element(by, value, timeout)
        return element.text if element else ""

    # ── Assertions ────────────────────────────────────────────────────────
    def is_element_visible(self, by, value, timeout=5):
        """Check if an element is visible."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(by, value)
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_text_present(self, text, timeout=5):
        """Check if text is present anywhere on the page."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                lambda d: text in d.page_source
            )
        except TimeoutException:
            return False

    def get_page_source(self):
        """Get the full page source."""
        return self.driver.page_source

    # ── JavaScript Execution ──────────────────────────────────────────────
    def execute_script(self, script, *args):
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, element):
        """Scroll element into view."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ── Screenshots ───────────────────────────────────────────────────────
    def take_screenshot(self, name: str) -> str:
        """Capture a screenshot with the given name."""
        return capture_screenshot(self.driver, name)

    # ── Window Management ─────────────────────────────────────────────────
    def set_viewport(self, width: int, height: int):
        """Set browser viewport size."""
        self.driver.set_window_size(width, height)

    def get_viewport_size(self):
        """Get current viewport dimensions."""
        return self.driver.get_window_size()

    # ── Browser Logs ──────────────────────────────────────────────────────
    def get_console_logs(self):
        """Get browser console logs."""
        try:
            return self.driver.get_log("browser")
        except Exception:
            return []

    def get_console_errors(self):
        """Get only error-level console logs."""
        logs = self.get_console_logs()
        return [log for log in logs if log.get("level") == "SEVERE"]

    # ── Performance ───────────────────────────────────────────────────────
    def get_page_load_time(self):
        """Get page load time in milliseconds."""
        try:
            timing = self.driver.execute_script(
                "var t = window.performance.timing; "
                "return t.loadEventEnd - t.navigationStart;"
            )
            return max(timing, 0)
        except Exception:
            return -1

    def get_resource_count(self):
        """Get number of resources loaded."""
        try:
            return self.driver.execute_script(
                "return window.performance.getEntriesByType('resource').length;"
            )
        except Exception:
            return -1

    def get_total_transfer_size(self):
        """Get total transfer size of all resources in bytes."""
        try:
            return self.driver.execute_script(
                "return window.performance.getEntriesByType('resource')"
                ".reduce((sum, r) => sum + (r.transferSize || 0), 0);"
            )
        except Exception:
            return -1
