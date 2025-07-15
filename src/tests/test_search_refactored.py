import pytest
from src.pages.home_page import HomePage
from src.pages.search_results_page import SearchResultsPage
from src.config.config import config
from src.utils.logger import logger

class TestSearchFunctionality:
    """Test suite for Amazon search functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup test pages"""
        self.page = page
        self.home_page = HomePage(page)
        self.search_results = SearchResultsPage(page)
        
    def test_basic_search(self):
        """Test basic search returns results"""
        # Navigate to Amazon
        self.home_page.goto()
        
        # Verify we're on homepage
        assert "amazon" in self.home_page.get_page_title().lower()
        
        # Perform search
        self.home_page.search_product(config.test_product)
        
        # Wait a bit for results to load
        self.page.wait_for_timeout(2000)
        
        # Verify results
        assert self.search_results.has_results(), f"No results found for {config.test_product}"
        
        results_count = self.search_results.get_results_count()
        logger.info(f"Found {results_count:,} results for {config.test_product}")
        assert results_count > 0, "Should have at least one result"
        
    def test_search_product_details(self):
        """Test extracting product details from search"""
        # Navigate and search
        self.home_page.goto()
        self.home_page.search_product("laptop")  # Use simpler search term
        
        # Wait for results
        self.page.wait_for_timeout(3000)
        
        # Get products
        products = self.search_results.get_products(max_count=5)
        
        # Verify we got products
        assert len(products) > 0, "Should extract at least one product"
        
        # Find a product with a title
        product_with_title = None
        for product in products:
            if product['title']:
                product_with_title = product
                break
                
        # Verify at least one product has a title
        assert product_with_title is not None, "Should find at least one product with title"
        
        # Log results
        logger.info(f"Found product: {product_with_title['title'][:50]}... - ${product_with_title['price']}")
        
    @pytest.mark.skip(reason="Skipping for now to focus on basic tests")
    def test_no_results_search(self):
        """Test search with no results"""
        pass
        
    @pytest.mark.skip(reason="Skipping for now to focus on basic tests")
    def test_search_result_consistency(self):
        """Test that search results are consistent"""
        pass