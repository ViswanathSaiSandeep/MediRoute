"""
Appium WebDriver factory – creates and configures the Appium driver for Android.
"""

import os
import sys
from appium import webdriver
from appium.options.android import UiAutomator2Options

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.appium_settings import (
    APPIUM_URL, PLATFORM_NAME, AUTOMATION_NAME,
    DEVICE_NAME, APP_PACKAGE, APP_ACTIVITY,
    PLATFORM_VERSION, APK_PATH,
    IMPLICIT_WAIT, APP_LAUNCH_TIMEOUT, NEW_COMMAND_TIMEOUT,
)


def create_appium_driver():
    """Create a configured Appium driver for Android."""
    options = UiAutomator2Options()

    options.platform_name = PLATFORM_NAME
    options.automation_name = AUTOMATION_NAME
    options.device_name = DEVICE_NAME
    options.platform_version = PLATFORM_VERSION
    options.new_command_timeout = NEW_COMMAND_TIMEOUT
    options.no_reset = False
    options.full_reset = False
    options.auto_grant_permissions = True

    if APK_PATH and os.path.exists(APK_PATH):
        options.app = os.path.abspath(APK_PATH)
    else:
        options.app_package = APP_PACKAGE
        options.app_activity = APP_ACTIVITY
        options.app_wait_activity = "*"
        options.app_wait_duration = APP_LAUNCH_TIMEOUT

    # Flutter-specific options
    options.set_capability("skipDeviceInitialization", False)
    options.set_capability("skipServerInstallation", False)
    options.set_capability("disableWindowAnimation", True)
    options.set_capability("uiautomator2ServerLaunchTimeout", 60000)
    options.set_capability("uiautomator2ServerInstallTimeout", 60000)

    driver = webdriver.Remote(APPIUM_URL, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver


def create_chrome_webview_driver():
    """Create an Appium driver for Chrome WebView testing on Android.
    Tests the Flutter web app via mobile Chrome browser."""
    from config.appium_settings import BASE_URL

    options = UiAutomator2Options()
    options.platform_name = PLATFORM_NAME
    options.automation_name = AUTOMATION_NAME
    options.device_name = DEVICE_NAME
    options.platform_version = PLATFORM_VERSION
    options.new_command_timeout = NEW_COMMAND_TIMEOUT
    options.no_reset = True

    # Use Chrome browser instead of native app
    options.set_capability("browserName", "Chrome")
    options.set_capability("chromedriverAutodownload", True)

    driver = webdriver.Remote(APPIUM_URL, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)

    # Navigate to the deployed web app
    driver.get(BASE_URL)

    return driver
