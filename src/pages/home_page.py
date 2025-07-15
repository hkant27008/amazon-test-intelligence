# Update src/pages/home_page.py

"""
Amazon Home Page Object
Contains all interactions specific to the Amazon homepage
"""

from src.pages.base_page import BasePage
from src.utils.logger import setup_logger

class HomePage(BasePage):
    """Amazon Homepage interactions"""
    
    def __init__(self, page):
        super().__init__(page)
        self.logger = setup_logger(self.__class__.__name__)
        
        # Element selectors
        self.SEARCH_BOX = "#twotabsearchtextbox"
        self.SEARCH_BUTTON = "#nav-search-submit-button"
        self.CART_COUNT = "#nav-cart-count"
        self.ACCOUNT_MENU = "#nav-link-accountList"
        self.LOGO = "#nav-logo"
        
    def goto(self) -> 'HomePage':
        """Navigate to Amazon homepage"""
        self.navigate("https://www.amazon.com")
        # Don't wait for networkidle - just wait for search box
        self.page.wait_for_selector(self.SEARCH_BOX, timeout=15000)
        return self
        
    def search_product(self, product: str) -> None:
        """
        Search for a product
        
        Args:
            product: Product name to search
        """
        self.logger.info(f"Searching for product: {product}")
        self.wait_and_fill(self.SEARCH_BOX, product)
        self.wait_and_click(self.SEARCH_BUTTON)
        # Wait for URL to change to search results
        self.page.wait_for_url("**/s?k=*", timeout=10000)
        
    def get_cart_count(self) -> int:
        """Get current cart item count"""
        try:
            count_text = self.get_text(self.CART_COUNT)
            return int(count_text) if count_text.isdigit() else 0
        except:
            self.logger.warning("Could not get cart count, returning 0")
            return 0
            
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        account_text = self.get_text(self.ACCOUNT_MENU)
        return not account_text.startswith("Hello, sign in")
        
    def click_cart(self) -> None:
        """Click on cart icon"""
        self.wait_and_click(self.CART_COUNT)
