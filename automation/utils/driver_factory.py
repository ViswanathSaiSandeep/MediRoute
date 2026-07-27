"""
WebDriver factory – creates and configures headless Chrome for CI/CD.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    HEADLESS, WINDOW_WIDTH, WINDOW_HEIGHT,
    IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT,
)


def create_driver() -> webdriver.Chrome:
    """Create a configured Chrome WebDriver instance."""
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--force-device-scale-factor=1")
    # Enable logging
    options.set_capability("goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"})

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    return driver


def create_driver_with_viewport(width: int, height: int) -> webdriver.Chrome:
    """Create a Chrome driver with a specific viewport size."""
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    return driver
