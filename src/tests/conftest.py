# src/tests/conftest.py
"""
Pytest configuration and fixtures
Fixtures are reusable test components
"""

import pytest
from playwright.sync_api import Page, Browser
from typing import Generator

@pytest.fixture(scope="function")
def page(browser: Browser) -> Generator[Page, None, None]:
    """
    Create a new page for each test
    'function' scope means fresh page per test
    """
    # Create new browser context (like incognito window)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    )
    
    # Create new page
    page = context.new_page()
    
    # Provide page to test
    yield page
    
    # Cleanup after test
    page.close()
    context.close()

    # src/tests/conftest.py
"""
Enhanced pytest configuration with better fixtures
"""

import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from typing import Generator
from src.config.config import config
from src.utils.logger import logger
import os

@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context configuration"""
    return {
        "viewport": config.viewport,
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args) -> Generator[BrowserContext, None, None]:
    """Create browser context for each test"""
    context = browser.new_context(**browser_context_args)
    
    # Add some basic cookies to appear more legitimate
    context.add_cookies([
        {
            "name": "session-id", 
            "value": "test-session",
            "domain": ".amazon.com",
            "path": "/"
        }
    ])
    
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create page for each test"""
    page = context.new_page()
    logger.info(f"Created new page for test")
    
    yield page
    
    # Capture info on failure
    if hasattr(page, "_test_failed") and page._test_failed:
        screenshot_path = os.path.join(
            "reports", "screenshots", 
            f"failure_{page._test_name}.png"
        )
        page.screenshot(path=screenshot_path)
        logger.error(f"Test failed, screenshot saved: {screenshot_path}")
    
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Mark test failure status"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            page._test_failed = True
            page._test_name = item.name