"""
Configuration settings for Google Maps Scraper
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ScraperConfig:
    """Configuration class for the Google Maps scraper"""

    # Google Maps API settings (Dual API support)
    google_maps_api_key: str = ""
    google_maps_api_key_2: str = ""

    # Rate limiting settings (to avoid bans)
    requests_per_minute: int = 30
    delay_between_requests: float = 2.0  # seconds
    max_retries: int = 3
    retry_delay: float = 5.0  # seconds

    # Search settings
    max_results_per_search: int = 200  # Increased to get maximum results
    search_radius: int = 50000  # meters (50km)

    # File paths
    niches_file: str = "input/niches.csv"
    locations_file: str = "input/locations.csv"
    output_file: str = "output/scraped_data.csv"
    temp_file: str = "output/temp_scraped_data.csv"
    progress_file: str = "output/progress.json"
    log_file: str = "logs/scraper.log"
    api_usage_file: str = "output/api_usage.json"

    # Data fields to scrape
    data_fields: List[str] = None

    # Email scraping settings
    enable_email_scraping: bool = True
    website_timeout: int = 10  # seconds
    max_pages_per_website: int = 3  # contact, about, home pages

    # API Limits (Free tier: 11K requests per month per API)
    max_monthly_requests_per_api: int = 11000  # Free tier limit
    max_daily_emails: int = 500  # Stop scraping after 500 emails per day
    max_daily_requests: int = 2000  # Deprecated, kept for compatibility
    enable_crash_recovery: bool = True
    backup_interval: int = 100  # Save backup every N records
    
    def __post_init__(self):
        if self.data_fields is None:
            self.data_fields = [
                "name",
                "niche",
                "address",
                "state",
                "phone_number",
                "website",
                "email",  # Added email field
                "result_url"
            ]

        # Load API keys from environment if not provided
        if not self.google_maps_api_key or not self.google_maps_api_key_2:
            # Try to load from .env file explicitly
            from dotenv import load_dotenv
            load_dotenv('.env')
            if not self.google_maps_api_key:
                self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
            if not self.google_maps_api_key_2:
                self.google_maps_api_key_2 = os.getenv("GOOGLE_MAPS_API_KEY2", "")
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []

        if not self.google_maps_api_key:
            errors.append("Google Maps API key 1 is required. Set GOOGLE_MAPS_API_KEY environment variable or update config.py")

        if not self.google_maps_api_key_2:
            errors.append("Google Maps API key 2 is required. Set GOOGLE_MAPS_API_KEY2 environment variable or update config.py")
        
        if self.requests_per_minute <= 0:
            errors.append("requests_per_minute must be positive")
            
        if self.delay_between_requests < 0:
            errors.append("delay_between_requests must be non-negative")
            
        if not os.path.exists(os.path.dirname(self.output_file)):
            try:
                os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create output directory: {e}")
        
        if not os.path.exists(os.path.dirname(self.log_file)):
            try:
                os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create log directory: {e}")
        
        return errors

# Global config instance
config = ScraperConfig()
