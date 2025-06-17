"""
Day 1: Basic smoke test to verify our setup works
This test will:
1. Open Amazon.com
2. Verify the page loaded
3. Take a screenshot as proof
"""

import pytest
from playwright.sync_api import Page

def test_amazon_homepage_loads(page: Page):
    """Test that Amazon homepage loads successfully"""
    # Navigate to Amazon
    page.goto("https://www.amazon.com", wait_until="domcontentloaded")
    
    # Wait for search box - we know this works from test 2
    page.wait_for_selector('#twotabsearchtextbox', timeout=30000)
    
    # Verify we're on Amazon
    assert "amazon" in page.title().lower(), f"Expected 'amazon' in title, got: {page.title()}"
    
    # Take screenshot for evidence
    page.screenshot(path="reports/screenshots/amazon_homepage.png")
    print("✅ Amazon homepage loaded successfully!")

def test_search_box_exists(page: Page):
    """Test that search box is present and functional"""
    # Navigate to Amazon
    page.goto("https://www.amazon.com", wait_until="domcontentloaded")
    
    # Check search box exists
    search_box = page.locator('#twotabsearchtextbox')
    assert search_box.is_visible(), "Search box should be visible"
    
    # Verify we can type in it
    search_box.fill("laptop")
    assert search_box.input_value() == "laptop", "Should be able to type in search box"
    
    print("✅ Search box is functional!")

def test_amazon_navigation_menu(page: Page):
    """Test that main navigation menu is present"""
    page.goto("https://www.amazon.com", wait_until="domcontentloaded")
    
    # Wait for page to load - use search box as indicator
    page.wait_for_selector('#twotabsearchtextbox', timeout=30000)
    
    # Check main elements exist (with more flexible selectors)
    cart = page.locator('#nav-cart, [aria-label*="cart"], [data-csa-c-content-id="nav_cart"]').first
    assert cart.is_visible(), "Cart should be visible"
    
    # Take screenshot of navigation
    page.screenshot(path="reports/screenshots/navigation_menu.png")
    print("✅ Navigation menu is present!")