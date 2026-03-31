"""
Bot Settings Manager - Handles all configurable bot settings
Stores settings in bot_settings.json
"""

import json
import os
from datetime import datetime
import logging


class BotSettingsManager:
    """Manages bot configuration settings"""
    
    SETTINGS_FILE = 'bot_settings.json'
    
    # Default settings
    DEFAULT_SETTINGS = {
        'email_sending_start_time': '08:00',  # HH:MM format, 24-hour
        'daily_email_limit': 100,
        'delay_between_emails': 600,  # seconds
        'timezone': 'Europe/London'
    }
    
    def __init__(self):
        self.logger = logging.getLogger('bot_settings')
        self.settings = self._load_settings()
    
    def _load_settings(self) -> dict:
        """Load settings from file or create with defaults"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged = {**self.DEFAULT_SETTINGS, **settings}
                return merged
            except Exception as e:
                self.logger.error(f"Error loading settings: {e}. Using defaults.")
                return self.DEFAULT_SETTINGS.copy()
        else:
            return self.DEFAULT_SETTINGS.copy()
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
            self.logger.info(f"Settings saved to {self.SETTINGS_FILE}")
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
    
    @staticmethod
    def _validate_time_format(time_str: str) -> bool:
        """Validate time format HH:MM (24-hour)"""
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            
            hours = int(parts[0])
            minutes = int(parts[1])
            
            if not (0 <= hours <= 23):
                return False
            if not (0 <= minutes <= 59):
                return False
            
            return True
        except (ValueError, AttributeError):
            return False
    
    def get_start_time(self) -> str:
        """Get email sending start time (HH:MM format)"""
        return self.settings.get('email_sending_start_time', '08:00')
    
    def get_daily_limit(self) -> int:
        """Get daily email limit"""
        return self.settings.get('daily_email_limit', 100)
    
    def get_delay_between_emails(self) -> int:
        """Get delay between emails in seconds"""
        return self.settings.get('delay_between_emails', 600)
    
    def get_timezone(self) -> str:
        """Get timezone"""
        return self.settings.get('timezone', 'Europe/London')
    
    def set_start_time(self, time_str: str) -> bool:
        """Set email sending start time. Returns True if successful."""
        if not self._validate_time_format(time_str):
            self.logger.error(f"Invalid time format: {time_str}. Use HH:MM (24-hour)")
            return False
        
        self.settings['email_sending_start_time'] = time_str
        self._save_settings()
        return True
    
    def set_daily_limit(self, limit: int) -> bool:
        """Set daily email limit. Returns True if successful."""
        if not isinstance(limit, int) or limit <= 0:
            self.logger.error(f"Invalid daily limit: {limit}. Must be positive integer")
            return False
        
        self.settings['daily_email_limit'] = limit
        self._save_settings()
        return True
    
    def set_delay_between_emails(self, delay: int) -> bool:
        """Set delay between emails in seconds. Returns True if successful."""
        if not isinstance(delay, int) or delay < 0:
            self.logger.error(f"Invalid delay: {delay}. Must be non-negative integer")
            return False
        
        self.settings['delay_between_emails'] = delay
        self._save_settings()
        return True
    
    def display_settings(self):
        """Display current settings"""
        tz = self.get_timezone()
        # Get friendly timezone name
        tz_display = tz.replace('_', ' ').replace('America/', '').replace('Europe/', '').replace('Asia/', '')

        print("\n" + "=" * 80)
        print("CURRENT BOT SETTINGS".center(80))
        print("=" * 80)
        print(f"Email Sending Start Time: {self.get_start_time()} ({tz_display} Time)")
        print(f"Daily Email Limit: {self.get_daily_limit()} emails")
        print(f"Delay Between Emails: {self.get_delay_between_emails()} seconds")
        print(f"Timezone: {tz}")
        print("=" * 80 + "\n")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self._save_settings()
        self.logger.info("Settings reset to defaults")

