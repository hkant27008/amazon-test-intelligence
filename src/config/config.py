# src/config/config.py
"""
Configuration management using environment variables
Centralizes all configuration in one place
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class TestConfig:
    """Test configuration settings"""
    
    # Basic settings
    base_url: str = os.getenv('BASE_URL', 'https://www.amazon.com')
    headless: bool = os.getenv('HEADLESS', 'False').lower() == 'true'
    timeout: int = int(os.getenv('TIMEOUT', '30000'))
    
    # Browser settings
    browser_type: str = os.getenv('BROWSER', 'chromium')
    viewport_width: int = int(os.getenv('VIEWPORT_WIDTH', '1920'))
    viewport_height: int = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
    
    # Test settings
    screenshot_on_failure: bool = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    retry_count: int = int(os.getenv('RETRY_COUNT', '2'))
    
    # Test data
    test_product: str = os.getenv('TEST_PRODUCT', 'laptop')
    test_category: str = os.getenv('TEST_CATEGORY', 'Electronics')
    
    @property
    def viewport(self) -> dict:
        """Get viewport configuration"""
        return {
            'width': self.viewport_width,
            'height': self.viewport_height
        }
        
    @property
    def is_ci(self) -> bool:
        """Check if running in CI environment"""
        return os.getenv('CI', 'false').lower() == 'true'

# Global config instance
config = TestConfig()