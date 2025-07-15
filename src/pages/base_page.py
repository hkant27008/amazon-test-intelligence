# Update src/pages/base_page.py to remove networkidle wait

"""
Base Page class with common functionality for all pages
This implements core methods that every page will need
"""

from playwright.sync_api import Page, expect
from typing import Optional, List
import logging
from datetime import datetime
import os

class BasePage:
    """
    Base page class containing common methods for all pages
    Follows DRY principle - Don't Repeat Yourself
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def navigate(self, url: str) -> None:
        """Navigate to a URL with logging"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        
    def wait_and_click(self, selector: str, timeout: int = 30000) -> None:
        """Wait for element and click with error handling"""
        try:
            self.logger.info(f"Clicking element: {selector}")
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click {selector}: {str(e)}")
            self.take_screenshot(f"click_failure_{selector.replace('/', '_')}")
            raise
            
    def wait_and_fill(self, selector: str, text: str, timeout: int = 30000) -> None:
        """Wait for element and fill text"""
        try:
            self.logger.info(f"Filling '{text}' in {selector}")
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            element.fill(text)
        except Exception as e:
            self.logger.error(f"Failed to fill {selector}: {str(e)}")
            self.take_screenshot("fill_failure")
            raise
            
    def get_text(self, selector: str, timeout: int = 30000) -> str:
        """Get text from element with wait"""
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element.text_content().strip()
        
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible without throwing exception"""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False
            
    def take_screenshot(self, name: str) -> str:
        """Take screenshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join("reports", "screenshots", filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        self.page.screenshot(path=filepath)
        self.logger.info(f"Screenshot saved: {filepath}")
        return filepath
        
    def wait_for_page_load(self) -> None:
        """Wait for page to be fully loaded - using domcontentloaded instead of networkidle"""
        self.page.wait_for_load_state("domcontentloaded")
        
    def get_page_title(self) -> str:
        """Get page title"""
        return self.page.title()
        
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.page.url
