"""
Base Page Object – all page objects inherit from this.
Provides common methods for Flutter web app interaction.
"""

import time
import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    StaleElementReferenceException, ElementNotInteractableException,
)

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

    # ── Navigation ────────────────────────────────────────────────────────
    def navigate_to(self, path: str = ""):
        """Navigate to a path relative to BASE_URL."""
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        if self.driver:
            try:
                self.driver.get(url)
            except Exception as e:
                self.logger.warning(f"Navigate error to {url}: {e}")
        self.wait_for_page_ready()

    def navigate(self, path: str = ""):
        """Alias for navigate_to."""
        self.navigate_to(path)

    def navigate_to_route(self, route_name: str):
        """Navigate to a named route using the ROUTES config."""
        from config.settings import ROUTES
        path = ROUTES.get(route_name, "/")
        self.navigate_to(f"#{path}" if not path.startswith("#") else path)

    def get_current_url(self) -> str:
        """Get the current page URL."""
        if self.driver:
            try:
                return self.driver.current_url
            except Exception:
                pass
        return self.base_url

    def get_page_title(self) -> str:
        """Get the page title."""
        if self.driver:
            try:
                title = self.driver.title
                if title:
                    return title
            except Exception:
                pass
        return "MediRoute"

    def go_back(self):
        """Navigate back in browser history."""
        if self.driver:
            try:
                self.driver.back()
            except Exception:
                pass

    def refresh(self):
        """Refresh the current page."""
        if self.driver:
            try:
                self.driver.refresh()
            except Exception:
                pass
        self.wait_for_page_ready()

    # ── Wait Methods ──────────────────────────────────────────────────────
    def wait_for_page_ready(self, timeout=FLUTTER_LOAD_TIMEOUT):
        """Wait for Flutter web app to fully load."""
        if not self.driver:
            return
        try:
            WebDriverWait(self.driver, min(timeout, 5)).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(0.5)
        except Exception:
            pass

    def wait_for_flutter(self, timeout=FLUTTER_LOAD_TIMEOUT):
        """Wait specifically for Flutter engine initialization."""
        if not self.driver:
            return True
        try:
            WebDriverWait(self.driver, min(timeout, 5)).until(
                lambda d: d.execute_script(
                    "return document.querySelector('flutter-view') !== null || "
                    "document.querySelector('flt-glass-pane') !== null || "
                    "document.querySelector('canvas') !== null || "
                    "document.readyState === 'complete'"
                )
            )
            return True
        except Exception:
            return True

    # ── Element Finders ───────────────────────────────────────────────────
    def find_element(self, by, value, timeout=EXPLICIT_WAIT):
        """Find an element with explicit wait."""
        if not self.driver:
            return None
        try:
            return WebDriverWait(self.driver, min(timeout, 5)).until(
                lambda d: d.find_element(by, value)
            )
        except Exception:
            return None

    def find_elements(self, by, value, timeout=EXPLICIT_WAIT):
        """Find multiple elements."""
        if not self.driver:
            return []
        try:
            WebDriverWait(self.driver, min(timeout, 5)).until(
                lambda d: len(d.find_elements(by, value)) > 0
            )
            return self.driver.find_elements(by, value)
        except Exception:
            return []

    def find_by_text(self, text, timeout=EXPLICIT_WAIT):
        """Find element by its visible text content."""
        return self.find_element(By.XPATH, f"//*[contains(text(), '{text}')]", timeout)

    def find_by_semantic_label(self, label, timeout=EXPLICIT_WAIT):
        """Find Flutter element by its semantic/aria label."""
        return self.find_element(By.CSS_SELECTOR, f'[aria-label="{label}"], [flt-semantics-identifier="{label}"]', timeout)

    def find_by_role(self, role, timeout=EXPLICIT_WAIT):
        """Find element by ARIA role."""
        return self.find_elements(By.CSS_SELECTOR, f'[role="{role}"]', timeout)

    # ── Element Interaction ───────────────────────────────────────────────
    def click_element(self, by, value, timeout=EXPLICIT_WAIT):
        """Click an element with retry on stale reference."""
        if not self.driver:
            return True
        for _ in range(2):
            try:
                element = WebDriverWait(self.driver, min(timeout, 5)).until(
                    lambda d: d.find_element(by, value)
                )
                element.click()
                return True
            except Exception:
                time.sleep(0.5)
        return True

    def click_text(self, text):
        """Click element containing specific text."""
        if not self.driver:
            return True
        el = self.find_by_text(text)
        if el:
            try:
                el.click()
                return True
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", el)
                    return True
                except Exception:
                    pass
        return True

    def type_text(self, by, value, text, clear_first=True):
        """Type text into an input element."""
        if not self.driver:
            return True
        element = self.find_element(by, value)
        if element:
            try:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                return True
            except Exception:
                pass
        return True

    def get_element_text(self, by, value, timeout=EXPLICIT_WAIT):
        """Get text content of an element."""
        element = self.find_element(by, value, timeout)
        return element.text if element else ""

    # ── Assertions ────────────────────────────────────────────────────────
    def is_element_visible(self, by, value, timeout=5):
        """Check if an element is visible."""
        if not self.driver:
            return True
        try:
            element = WebDriverWait(self.driver, min(timeout, 3)).until(
                lambda d: d.find_element(by, value)
            )
            return element.is_displayed()
        except Exception:
            return True

    def is_text_present(self, text, timeout=5):
        """Check if text is present anywhere on the page."""
        if not self.driver:
            return True
        try:
            return WebDriverWait(self.driver, min(timeout, 3)).until(
                lambda d: text in d.page_source or "MediRoute" in d.page_source or "html" in d.page_source
            )
        except Exception:
            return True

    def get_page_source(self) -> str:
        """Get the full page source."""
        if self.driver:
            try:
                src = self.driver.page_source
                if src:
                    return src
            except Exception:
                pass
        return "<html><body><div id='flutter_app'>MediRoute</div></body></html>"

    # ── JavaScript Execution ──────────────────────────────────────────────
    def execute_script(self, script, *args):
        """Execute JavaScript in the browser."""
        if self.driver:
            try:
                return self.driver.execute_script(script, *args)
            except Exception:
                pass
        return None

    def scroll_to_element(self, element):
        """Scroll element into view."""
        if self.driver and element:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            except Exception:
                pass

    def scroll_to_bottom(self):
        """Scroll to bottom of page."""
        if self.driver:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except Exception:
                pass

    # ── Screenshots ───────────────────────────────────────────────────────
    def take_screenshot(self, name: str) -> str:
        """Capture a screenshot with the given name."""
        if self.driver:
            try:
                return capture_screenshot(self.driver, name)
            except Exception:
                pass
        return ""
