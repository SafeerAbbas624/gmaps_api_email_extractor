"""
Simple Email Manager - One file for everything
Manages unique emails and tracks sent emails
"""

import json
import os
import re
from datetime import datetime
from typing import Set, List, Dict
import pytz
from bot_settings import BotSettingsManager


class SimpleEmailManager:
    """Manages all emails in one simple file"""

    def __init__(self, email_file='emails.json'):
        self.email_file = email_file
        # Load timezone from bot_settings.json
        settings = BotSettingsManager()
        self.configured_tz = pytz.timezone(settings.get_timezone())
        self.data = self._load_data()

    def _get_current_date(self) -> str:
        """Get current date in configured timezone (YYYY-MM-DD format)"""
        now_tz = datetime.now(self.configured_tz)
        return now_tz.strftime('%Y-%m-%d')

    def _load_data(self) -> Dict:
        """Load email data from file"""
        if os.path.exists(self.email_file):
            try:
                with open(self.email_file, 'r') as f:
                    data = json.load(f)
                    # Upgrade old data structure to include daily_tracking if missing
                    return self._upgrade_data_structure(data)
            except:
                pass

        # Default structure
        return {
            'all_emails': {},  # email -> {business_name, added_date, sent_date, sent_count}
            'stats': {
                'total_collected': 0,
                'total_sent': 0,
                'total_failed': 0
            },
            'daily_limit_info': {
                'last_limit_hit': None,  # When we hit Gmail's daily limit
                'resume_after': None  # When we can resume sending (24h from last successful email)
            },
            'daily_tracking': {
                'date': self._get_current_date(),  # Current date in configured timezone
                'sent_today': 0,  # Emails sent today (persisted to disk)
                'failed_today': 0,  # Emails failed today (persisted to disk)
                'last_email_sent_time': None  # Track last email send time for rate limiting
            }
        }

    def _upgrade_data_structure(self, data: Dict) -> Dict:
        """Upgrade old data structure to include new fields"""
        # Add daily_tracking if missing
        if 'daily_tracking' not in data:
            data['daily_tracking'] = {
                'date': self._get_current_date(),  # Use configured timezone
                'sent_today': 0,
                'failed_today': 0,
                'last_email_sent_time': None
            }
        else:
            # Add last_email_sent_time if missing from existing daily_tracking
            if 'last_email_sent_time' not in data['daily_tracking']:
                data['daily_tracking']['last_email_sent_time'] = None

        # Add daily_limit_info if missing
        if 'daily_limit_info' not in data:
            data['daily_limit_info'] = {
                'last_limit_hit': None,
                'resume_after': None
            }

        # Add stats if missing
        if 'stats' not in data:
            data['stats'] = {
                'total_collected': 0,
                'total_sent': 0,
                'total_failed': 0
            }

        return data

    def reload_data(self):
        """Reload email data from disk - CRITICAL for multi-process safety"""
        self.data = self._load_data()
    
    def _save_data(self):
        """Save email data to file"""
        try:
            with open(self.email_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving email data: {e}")
    
    def is_valid_email(self, email: str) -> bool:
        """Check if email is valid"""
        if not email or email == 'nan' or str(email).lower() == 'nan':
            return False
        
        # Basic email regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))
    
    def add_email(self, email: str, business_name: str = '') -> bool:
        """Add a new email if it's valid and unique"""
        if not self.is_valid_email(email):
            return False

        email = email.lower().strip()

        # CRITICAL FIX: Reload from disk before checking to prevent duplicates in multi-process environment
        self.reload_data()

        # Check if already exists (including already-sent emails)
        if email in self.data['all_emails']:
            # Email already exists - don't add it again
            # This prevents duplicate sends even if email was sent by another process
            return False

        # Add new email
        self.data['all_emails'][email] = {
            'business_name': business_name,
            'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sent_date': None,
            'sent_count': 0,
            'failed_count': 0
        }

        self.data['stats']['total_collected'] += 1
        self._save_data()
        return True
    
    def get_unsent_emails(self, limit: int = None) -> List[str]:
        """Get emails that haven't been sent yet"""
        # CRITICAL FIX: Reload from disk before checking to prevent sending duplicates
        self.reload_data()

        unsent = [
            email for email, info in self.data['all_emails'].items()
            if info['sent_count'] == 0
        ]

        if limit:
            return unsent[:limit]
        return unsent
    
    def mark_as_sent(self, email: str, success: bool = True):
        """Mark an email as sent"""
        email = email.lower().strip()

        # CRITICAL FIX: Reload from disk before marking to ensure accurate state
        self.reload_data()

        if email not in self.data['all_emails']:
            return

        # Check if this email was already sent before
        was_already_sent = self.data['all_emails'][email]['sent_count'] > 0

        if success:
            self.data['all_emails'][email]['sent_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.data['all_emails'][email]['sent_count'] += 1

            # Only increment total_sent if this is the FIRST time sending this email
            if not was_already_sent:
                self.data['stats']['total_sent'] += 1
        else:
            self.data['all_emails'][email]['failed_count'] += 1

            # Only increment total_failed if this email was never sent successfully
            if not was_already_sent:
                self.data['stats']['total_failed'] += 1

        self._save_data()

        # Update daily tracking (persisted to disk)
        self._update_daily_tracking(success)

    def _update_daily_tracking(self, success: bool = True):
        """Update daily sent/failed counts and last email send time (persisted to disk)"""
        # CRITICAL FIX: Reload to ensure we have latest daily tracking
        self.reload_data()

        current_date = self._get_current_date()  # Use configured timezone
        now_tz = datetime.now(self.configured_tz)
        current_time = now_tz.strftime('%Y-%m-%d %H:%M:%S')

        # Check if date changed (in configured timezone)
        if self.data['daily_tracking']['date'] != current_date:
            # Reset for new day
            self.data['daily_tracking']['date'] = current_date
            self.data['daily_tracking']['sent_today'] = 0
            self.data['daily_tracking']['failed_today'] = 0
            self.data['daily_tracking']['last_email_sent_time'] = None

        # Update counts
        if success:
            self.data['daily_tracking']['sent_today'] += 1
            # Save the time of last successful email send
            self.data['daily_tracking']['last_email_sent_time'] = current_time
        else:
            self.data['daily_tracking']['failed_today'] += 1

        self._save_data()

    def get_daily_stats(self) -> dict:
        """Get today's sent/failed counts (persisted to disk)"""
        # CRITICAL FIX: Reload to ensure we have latest daily tracking
        self.reload_data()

        current_date = self._get_current_date()  # Use configured timezone

        # Check if date changed (in configured timezone)
        if self.data['daily_tracking']['date'] != current_date:
            # Reset for new day
            self.data['daily_tracking']['date'] = current_date
            self.data['daily_tracking']['sent_today'] = 0
            self.data['daily_tracking']['failed_today'] = 0
            self._save_data()

        return {
            'date': self.data['daily_tracking']['date'],
            'sent_today': self.data['daily_tracking']['sent_today'],
            'failed_today': self.data['daily_tracking']['failed_today']
        }

    def get_last_successful_email_time(self) -> str:
        """Get the time of the last successfully sent email from the data"""
        last_time = None

        for email, info in self.data['all_emails'].items():
            if info['sent_count'] > 0 and info['sent_date']:
                if last_time is None or info['sent_date'] > last_time:
                    last_time = info['sent_date']

        return last_time

    def set_daily_limit_hit(self, last_successful_email_time: str = None):
        """Mark that we hit the daily limit"""
        # If no time provided, try to get from data
        if last_successful_email_time is None:
            last_successful_email_time = self.get_last_successful_email_time()

        # If still None, use current time
        if last_successful_email_time is None:
            last_successful_email_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Calculate resume time (24 hours from last successful email)
        from datetime import timedelta
        last_time = datetime.strptime(last_successful_email_time, '%Y-%m-%d %H:%M:%S')
        resume_time = last_time + timedelta(hours=24)

        self.data['daily_limit_info']['last_limit_hit'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.data['daily_limit_info']['resume_after'] = resume_time.strftime('%Y-%m-%d %H:%M:%S')
        self._save_data()

    def can_send_emails(self) -> tuple[bool, str]:
        """Check if we can send emails (not in 24h wait period)"""
        # CRITICAL FIX: Reload from disk to get latest daily limit info
        self.reload_data()

        resume_after = self.data.get('daily_limit_info', {}).get('resume_after')

        if not resume_after:
            return True, ""

        resume_time = datetime.strptime(resume_after, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()

        if now < resume_time:
            time_left = resume_time - now
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)
            return False, f"Wait {hours}h {minutes}m (resume at {resume_after})"

        # Clear the limit info since we can send now
        self.data['daily_limit_info']['last_limit_hit'] = None
        self.data['daily_limit_info']['resume_after'] = None
        self._save_data()
        return True, ""

    def get_stats(self) -> Dict:
        """Get statistics"""
        unsent_count = len(self.get_unsent_emails())

        return {
            'total_collected': self.data['stats']['total_collected'],
            'total_sent': self.data['stats']['total_sent'],
            'total_failed': self.data['stats']['total_failed'],
            'unsent': unsent_count
        }
    
    def import_from_csv(self, csv_file: str) -> int:
        """Import emails from CSV file"""
        import csv
        
        if not os.path.exists(csv_file):
            return 0
        
        added_count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('email', '')
                    name = row.get('name', '')
                    
                    if self.add_email(email, name):
                        added_count += 1
        except Exception as e:
            print(f"Error importing from CSV: {e}")
        
        return added_count


def main():
    """Test the email manager"""
    manager = SimpleEmailManager()
    
    # Import from CSV
    print("Importing emails from CSV...")
    added = manager.import_from_csv('output/scraped_data.csv')
    print(f"Added {added} new unique valid emails")
    
    # Show stats
    stats = manager.get_stats()
    print(f"\nStats:")
    print(f"  Total collected: {stats['total_collected']}")
    print(f"  Total sent: {stats['total_sent']}")
    print(f"  Total failed: {stats['total_failed']}")
    print(f"  Unsent: {stats['unsent']}")
    
    # Show unsent emails
    unsent = manager.get_unsent_emails(limit=10)
    print(f"\nFirst 10 unsent emails:")
    for email in unsent:
        info = manager.data['all_emails'][email]
        print(f"  {email} - {info['business_name']}")


if __name__ == '__main__':
    main()

