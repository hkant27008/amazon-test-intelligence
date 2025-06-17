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