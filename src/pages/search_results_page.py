"""
Amazon Search Results Page Object
Handles interactions with search results
"""

from src.pages.base_page import BasePage
from src.utils.logger import setup_logger
from typing import List, Dict, Optional
import re

class SearchResultsPage(BasePage):
    """Search results page interactions"""
    
    def __init__(self, page):
        super().__init__(page)
        self.logger = setup_logger(self.__class__.__name__)
        
        # Element selectors - updated for better reliability
        self.RESULTS_INFO = '[data-component-type="s-result-info-bar"]'
        self.PRODUCT_CARDS = '[data-component-type="s-search-result"]'
        self.PRODUCT_TITLE = 'h2 span'  # Simplified selector
        self.PRODUCT_PRICE = '.a-price-whole'
        self.PRODUCT_RATING = '[aria-label*="out of 5 stars"]'
        self.NO_RESULTS_MESSAGE = '.s-no-results-message'
        self.NEXT_PAGE = '.s-pagination-next'
        self.SORT_DROPDOWN = '#s-result-sort-select'
        
    def get_results_count(self) -> int:
        """Get total number of results"""
        try:
            info_text = self.get_text(self.RESULTS_INFO)
            # Extract number from "1-48 of over 10,000 results"
            match = re.search(r'of\s+(?:over\s+)?([\d,]+)\s+results', info_text)
            if match:
                return int(match.group(1).replace(',', ''))
        except Exception as e:
            self.logger.error(f"Could not extract results count: {e}")
        return 0
        
    def has_results(self) -> bool:
        """Check if search returned results"""
        return not self.is_visible(self.NO_RESULTS_MESSAGE)
        
    def get_products(self, max_count: int = 10) -> List[Dict[str, any]]:
        """
        Extract product information from search results
        
        Args:
            max_count: Maximum number of products to extract
            
        Returns:
            List of product dictionaries
        """
        products = []
        product_elements = self.page.locator(self.PRODUCT_CARDS).all()[:max_count]
        
        for idx, element in enumerate(product_elements):
            try:
                # Try multiple selectors for title
                title = ""
                title_selectors = ['h2 span', 'h2 a span', 'h2', '.s-size-medium']
                
                for selector in title_selectors:
                    try:
                        title_elem = element.locator(selector).first
                        if title_elem.is_visible():
                            title = title_elem.text_content().strip()
                            if title:
                                break
                    except:
                        continue
                
                product = {
                    'index': idx + 1,
                    'title': title,
                    'price': self._extract_price(element),
                    'rating': self._extract_rating(element),
                    'is_prime': self._check_prime(element),
                    'is_sponsored': 'Sponsored' in element.text_content()
                }
                products.append(product)
                
                # Log what we found
                self.logger.info(f"Extracted product {idx + 1}: {title[:50] if title else 'No title'}...")
                
            except Exception as e:
                self.logger.warning(f"Failed to extract product {idx + 1}: {e}")
                
        return products
        
    def _check_prime(self, element) -> bool:
        """Check if product has Prime"""
        try:
            return element.locator('[aria-label="Amazon Prime"]').is_visible()
        except:
            return False
            
    def _extract_price(self, element) -> Optional[float]:
        """Extract price as float"""
        try:
            price_elem = element.locator(self.PRODUCT_PRICE).first
            if price_elem.is_visible():
                price_text = price_elem.text_content()
                # Remove currency symbols and convert to float
                price = re.sub(r'[^\d.]', '', price_text)
                return float(price) if price else None
        except:
            return None
            
    def _extract_rating(self, element) -> Optional[float]:
        """Extract rating value"""
        try:
            rating_elem = element.locator(self.PRODUCT_RATING).first
            if rating_elem.is_visible():
                aria_label = rating_elem.get_attribute('aria-label')
                match = re.search(r'([\d.]+) out of 5 stars', aria_label)
                if match:
                    return float(match.group(1))
        except:
            return None
            
    def click_product(self, index: int = 1) -> None:
        """Click on a product by index"""
        product = self.page.locator(self.PRODUCT_CARDS).nth(index - 1)
        product.locator('h2 a').first.click()
        self.wait_for_page_load()
        
    def sort_by(self, option: str) -> None:
        """Sort results by given option"""
        self.page.select_option(self.SORT_DROPDOWN, option)
        self.wait_for_page_load()