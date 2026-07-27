"""
Base Screen – all Appium page objects inherit from this.
Provides common methods for interacting with Flutter Android app elements.
"""

import time
import logging
import os
import sys

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    StaleElementReferenceException,
)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.appium_settings import EXPLICIT_WAIT, SCREENSHOTS_DIR


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


class BaseScreen:
    """Base class for all Appium Page Objects in MediRoute."""

    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

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
        """Find element by visible text (UiAutomator2)."""
        try:
            return self.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{text}")',
                timeout
            )
        except Exception:
            return None

    def find_by_content_desc(self, desc, timeout=EXPLICIT_WAIT):
        """Find element by content description / accessibility label."""
        try:
            return self.find_element(
                AppiumBy.ACCESSIBILITY_ID, desc, timeout
            )
        except Exception:
            return None

    def find_by_resource_id(self, resource_id, timeout=EXPLICIT_WAIT):
        """Find element by Android resource ID."""
        return self.find_element(AppiumBy.ID, resource_id, timeout)

    def find_by_class(self, class_name, timeout=EXPLICIT_WAIT):
        """Find elements by class name."""
        return self.find_elements(AppiumBy.CLASS_NAME, class_name, timeout)

    def find_by_xpath(self, xpath, timeout=EXPLICIT_WAIT):
        """Find element by XPath."""
        return self.find_element(AppiumBy.XPATH, xpath, timeout)

    # ── Element Interaction ───────────────────────────────────────────────
    def click_element(self, by, value, timeout=EXPLICIT_WAIT):
        """Click an element with retry on stale reference."""
        for attempt in range(3):
            try:
                el = self.find_element(by, value, timeout)
                if el:
                    el.click()
                    return True
            except (StaleElementReferenceException, Exception):
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
                pass
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

    def get_element_attribute(self, by, value, attribute, timeout=EXPLICIT_WAIT):
        """Get an attribute of an element."""
        element = self.find_element(by, value, timeout)
        return element.get_attribute(attribute) if element else ""

    # ── Assertions ────────────────────────────────────────────────────────
    def is_element_visible(self, by, value, timeout=5):
        """Check if an element is visible."""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(by, value)
            )
            return el.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_text_present(self, text, timeout=5):
        """Check if text is present on screen."""
        try:
            return self.find_by_text(text, timeout) is not None
        except Exception:
            return False

    def is_element_enabled(self, by, value, timeout=5):
        """Check if an element is enabled."""
        try:
            el = self.find_element(by, value, timeout)
            return el.is_enabled() if el else False
        except Exception:
            return False

    # ── Navigation ────────────────────────────────────────────────────────
    def go_back(self):
        """Press Android back button."""
        self.driver.back()

    def press_home(self):
        """Press Android home button."""
        self.driver.press_keycode(3)

    def press_enter(self):
        """Press enter key."""
        self.driver.press_keycode(66)

    def press_tab(self):
        """Press tab key."""
        self.driver.press_keycode(61)

    # ── Gestures ──────────────────────────────────────────────────────────
    def scroll_down(self):
        """Scroll down on the current screen."""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def scroll_up(self):
        """Scroll up on the current screen."""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.2)
        end_y = int(size['height'] * 0.8)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def scroll_to_text(self, text):
        """Scroll until text is visible (UiAutomator2)."""
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().textContains("{text}"))'
            )
            return True
        except Exception:
            return False

    def swipe_left(self):
        """Swipe left."""
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.8)
        end_x = int(size['width'] * 0.2)
        y = size['height'] // 2
        self.driver.swipe(start_x, y, end_x, y, 500)

    def swipe_right(self):
        """Swipe right."""
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.2)
        end_x = int(size['width'] * 0.8)
        y = size['height'] // 2
        self.driver.swipe(start_x, y, end_x, y, 500)

    def tap_coordinates(self, x, y):
        """Tap at specific screen coordinates."""
        self.driver.tap([(x, y)])

    # ── Screenshots ───────────────────────────────────────────────────────
    def take_screenshot(self, name: str) -> str:
        """Capture a screenshot."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(SCREENSHOTS_DIR, filename)
        try:
            self.driver.save_screenshot(filepath)
            return filepath
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return ""

    # ── App Management ────────────────────────────────────────────────────
    def get_current_activity(self):
        """Get the current Android activity."""
        try:
            return self.driver.current_activity
        except Exception:
            return ""

    def get_current_package(self):
        """Get the current Android package."""
        try:
            return self.driver.current_package
        except Exception:
            return ""

    def is_app_installed(self, package):
        """Check if an app is installed."""
        try:
            return self.driver.is_app_installed(package)
        except Exception:
            return False

    def get_page_source(self):
        """Get the XML page source."""
        try:
            return self.driver.page_source
        except Exception:
            return ""

    # ── Wait Methods ──────────────────────────────────────────────────────
    def wait_for_screen_ready(self, timeout=10):
        """Wait for the screen to be interactive."""
        time.sleep(2)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(AppiumBy.XPATH, "//*")) > 0
            )
            return True
        except TimeoutException:
            return False

    def wait_for_text(self, text, timeout=EXPLICIT_WAIT):
        """Wait for specific text to appear on screen."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textContains("{text}")'
                )
            )
            return True
        except TimeoutException:
            return False

    # ── Device Info ───────────────────────────────────────────────────────
    def get_device_info(self):
        """Get device information."""
        return {
            "platform": self.driver.capabilities.get("platformName", ""),
            "version": self.driver.capabilities.get("platformVersion", ""),
            "device": self.driver.capabilities.get("deviceName", ""),
            "screen_size": self.driver.get_window_size(),
        }

    def get_screen_size(self):
        """Get device screen dimensions."""
        return self.driver.get_window_size()

    def get_orientation(self):
        """Get device orientation."""
        try:
            return self.driver.orientation
        except Exception:
            return "UNKNOWN"

    def set_orientation(self, orientation):
        """Set device orientation (LANDSCAPE/PORTRAIT)."""
        try:
            self.driver.orientation = orientation
        except Exception:
            pass

    # ── Performance ───────────────────────────────────────────────────────
    def get_performance_data(self, package, data_type):
        """Get performance data from the device."""
        try:
            return self.driver.get_performance_data(package, data_type, 5)
        except Exception:
            return []
