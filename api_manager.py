"""
API Manager for handling dual Google Maps API keys with usage tracking
"""
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
import googlemaps
from config import config

class APIManager:
    """Manages dual API keys with daily and monthly usage tracking"""
    
    def __init__(self):
        self.logger = logging.getLogger("gmaps_scraper.api_manager")
        self.api_key_1 = config.google_maps_api_key
        self.api_key_2 = config.google_maps_api_key_2
        self.current_api = 1
        self.gmaps_1 = None
        self.gmaps_2 = None
        self.usage_file = config.api_usage_file
        self.usage_data = self._load_usage_data()
        
        # Initialize both API clients
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize both Google Maps clients"""
        try:
            if self.api_key_1:
                self.gmaps_1 = googlemaps.Client(key=self.api_key_1)
                self.logger.info("✅ API Key 1 initialized successfully")
            else:
                self.logger.error("❌ API Key 1 not found")
            
            if self.api_key_2:
                self.gmaps_2 = googlemaps.Client(key=self.api_key_2)
                self.logger.info("✅ API Key 2 initialized successfully")
            else:
                self.logger.error("❌ API Key 2 not found")
        except Exception as e:
            self.logger.error(f"Failed to initialize API clients: {e}")
            raise
    
    def _load_usage_data(self) -> Dict[str, Any]:
        """Load API usage data from file"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load usage file: {e}")
        
        return {
            "api_1": {"daily_requests": 0, "monthly_requests": 0, "last_date": None, "last_month": None},
            "api_2": {"daily_requests": 0, "monthly_requests": 0, "last_date": None, "last_month": None},
            "daily_emails": 0,
            "last_email_date": None
        }
    
    def _save_usage_data(self):
        """Save API usage data to file"""
        try:
            os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save usage data: {e}")
    
    def _reset_daily_if_needed(self, api_num: int):
        """Reset daily counters if it's a new day"""
        today = datetime.now().date().isoformat()
        api_key = f"api_{api_num}"
        
        if self.usage_data[api_key]["last_date"] != today:
            self.usage_data[api_key]["daily_requests"] = 0
            self.usage_data[api_key]["last_date"] = today
            self.logger.info(f"🔄 Reset daily counter for API {api_num}")
    
    def _reset_monthly_if_needed(self, api_num: int):
        """Reset monthly counters if it's a new month"""
        current_month = datetime.now().strftime("%Y-%m")
        api_key = f"api_{api_num}"
        
        if self.usage_data[api_key]["last_month"] != current_month:
            self.usage_data[api_key]["monthly_requests"] = 0
            self.usage_data[api_key]["last_month"] = current_month
            self.logger.info(f"🔄 Reset monthly counter for API {api_num}")
    
    def _reset_daily_emails_if_needed(self):
        """Reset daily email counter if it's a new day"""
        today = datetime.now().date().isoformat()
        
        if self.usage_data["last_email_date"] != today:
            self.usage_data["daily_emails"] = 0
            self.usage_data["last_email_date"] = today
            self.logger.info("🔄 Reset daily email counter")
    
    def get_current_client(self) -> googlemaps.Client:
        """Get the current API client"""
        if self.current_api == 1:
            return self.gmaps_1
        else:
            return self.gmaps_2
    
    def record_request(self):
        """Record a request for the current API"""
        api_num = self.current_api
        api_key = f"api_{api_num}"
        
        self._reset_daily_if_needed(api_num)
        self._reset_monthly_if_needed(api_num)
        
        self.usage_data[api_key]["daily_requests"] += 1
        self.usage_data[api_key]["monthly_requests"] += 1
        self._save_usage_data()
    
    def record_email_found(self):
        """Record that an email was found"""
        self._reset_daily_emails_if_needed()
        self.usage_data["daily_emails"] += 1
        self._save_usage_data()
    
    def check_daily_email_limit(self) -> bool:
        """Check if daily email limit is reached"""
        self._reset_daily_emails_if_needed()
        if self.usage_data["daily_emails"] >= config.max_daily_emails:
            self.logger.warning(f"⚠️  Daily email limit reached ({config.max_daily_emails} emails)")
            return True
        return False
    
    def check_monthly_limit(self) -> Tuple[bool, bool]:
        """Check if monthly limits are reached for both APIs. Returns (api1_limit_reached, api2_limit_reached)"""
        self._reset_monthly_if_needed(1)
        self._reset_monthly_if_needed(2)
        
        api1_limit = self.usage_data["api_1"]["monthly_requests"] >= config.max_monthly_requests_per_api
        api2_limit = self.usage_data["api_2"]["monthly_requests"] >= config.max_monthly_requests_per_api
        
        if api1_limit:
            self.logger.warning(f"⚠️  API 1 monthly limit reached ({config.max_monthly_requests_per_api} requests)")
        if api2_limit:
            self.logger.warning(f"⚠️  API 2 monthly limit reached ({config.max_monthly_requests_per_api} requests)")
        
        return api1_limit, api2_limit
    
    def switch_api(self) -> bool:
        """Switch to the other API. Returns True if switch successful, False if both APIs are at limit"""
        api1_limit, api2_limit = self.check_monthly_limit()
        
        if api1_limit and api2_limit:
            self.logger.error("❌ Both APIs have reached monthly limit!")
            return False
        
        if self.current_api == 1 and not api2_limit:
            self.current_api = 2
            self.logger.info("🔄 Switched to API 2")
            return True
        elif self.current_api == 2 and not api1_limit:
            self.current_api = 1
            self.logger.info("🔄 Switched to API 1")
            return True
        
        return False
    
    def get_status(self) -> str:
        """Get current API usage status"""
        self._reset_daily_if_needed(1)
        self._reset_daily_if_needed(2)
        self._reset_monthly_if_needed(1)
        self._reset_monthly_if_needed(2)
        self._reset_daily_emails_if_needed()
        
        status = f"""
╔════════════════════════════════════════════════════════════════╗
║                    API USAGE STATUS                            ║
╠════════════════════════════════════════════════════════════════╣
║ API 1:                                                         ║
║   Daily Requests:   {self.usage_data['api_1']['daily_requests']:>5} / ∞                                  ║
║   Monthly Requests: {self.usage_data['api_1']['monthly_requests']:>5} / {config.max_monthly_requests_per_api}                          ║
║                                                                ║
║ API 2:                                                         ║
║   Daily Requests:   {self.usage_data['api_2']['daily_requests']:>5} / ∞                                  ║
║   Monthly Requests: {self.usage_data['api_2']['monthly_requests']:>5} / {config.max_monthly_requests_per_api}                          ║
║                                                                ║
║ Emails Found Today: {self.usage_data['daily_emails']:>5} / {config.max_daily_emails}                          ║
║ Current API:        {self.current_api}                                                    ║
╚════════════════════════════════════════════════════════════════╝
"""
        return status

