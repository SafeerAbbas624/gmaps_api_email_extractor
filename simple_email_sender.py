"""
Simple Email Sender - Uses simple_email_manager.py
Sends emails to unique, unsent emails only
"""

import smtplib
import time
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from simple_email_manager import SimpleEmailManager
from datetime import datetime, timedelta
from email_messages import get_random_message
import pytz
from bot_settings import BotSettingsManager


class SimpleEmailSender:
    """Simple email sender using email manager"""

    def __init__(self):
        self.logger = self._setup_logging()
        self.email_manager = SimpleEmailManager()
        self.sender_email = None
        self.sender_password = None
        self.email_subject = None
        self.message_content = None

        # Load settings from bot_settings.json
        self.settings_manager = BotSettingsManager()
        self.daily_limit = self.settings_manager.get_daily_limit()
        self.delay_between_emails = self.settings_manager.get_delay_between_emails()
        self.email_sending_start_time = self.settings_manager.get_start_time()  # HH:MM format

        self.last_successful_email_time = None  # Track last successful email
        # Use timezone from settings (defaults to America/New_York)
        self.configured_tz = pytz.timezone(self.settings_manager.get_timezone())

        # Daily stats tracking (now persisted to disk via email_manager)
        self.session_start_time = datetime.now()
    
    def _setup_logging(self):
        """Setup logging"""
        import os
        os.makedirs("logs", exist_ok=True)

        logger = logging.getLogger('simple_email_sender')
        logger.setLevel(logging.INFO)

        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler('logs/email_sender.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _is_scraper_complete(self) -> bool:
        """Check if scraper has completed all combinations"""
        return os.path.exists("scraper_complete.flag")

    def _wait_until_start_time(self):
        """
        Wait until configured start time in the configured timezone before sending first email of the day.
        If already past start time, return immediately.
        """
        # Parse start time from HH:MM format
        try:
            start_hour, start_minute = map(int, self.email_sending_start_time.split(':'))
        except (ValueError, AttributeError):
            self.logger.error(f"Invalid start time format: {self.email_sending_start_time}. Using 08:00")
            start_hour, start_minute = 8, 0

        # Get timezone display name
        tz_name = self.settings_manager.get_timezone()
        tz_display = tz_name.replace('_', ' ').replace('America/', '').replace('Europe/', '').replace('Asia/', '')

        # Get current time in configured timezone
        now_tz = datetime.now(self.configured_tz)
        today_start = now_tz.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

        # If it's already past start time, we can send immediately
        if now_tz >= today_start:
            self.logger.info(f"Current {tz_display} time: {now_tz.strftime('%Y-%m-%d %H:%M:%S %Z')} - Past {self.email_sending_start_time}, can send emails")
            return

        # Calculate wait time until start time
        wait_duration = today_start - now_tz
        wait_seconds = int(wait_duration.total_seconds())
        wait_hours = wait_seconds // 3600
        wait_minutes = (wait_seconds % 3600) // 60

        self.logger.info("=" * 80)
        self.logger.info(f"Current {tz_display} time: {now_tz.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        self.logger.info(f"Waiting until {self.email_sending_start_time} {tz_display} time to start sending emails")
        self.logger.info(f"Wait time: {wait_hours}h {wait_minutes}m")
        self.logger.info("=" * 80)

        # Wait until start time
        while True:
            now_tz = datetime.now(self.configured_tz)
            today_start = now_tz.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

            if now_tz >= today_start:
                self.logger.info(f"{self.email_sending_start_time} {tz_display} time reached! Starting email sending...")
                break

            # Sleep for 1 minute and check again
            time.sleep(60)

    def _check_and_log_daily_summary(self):
        """Check if day changed and log daily summary"""
        # Get current daily stats from disk
        daily_stats = self.email_manager.get_daily_stats()
        current_date = datetime.now().strftime('%Y-%m-%d')

        if daily_stats['date'] != current_date:
            # Log previous day summary
            self._log_daily_summary()

            # Reset session start time for new day
            self.session_start_time = datetime.now()

    def _log_daily_summary(self):
        """Log daily summary"""
        runtime = datetime.now() - self.session_start_time
        hours = int(runtime.total_seconds() // 3600)
        minutes = int((runtime.total_seconds() % 3600) // 60)

        # Get daily stats from disk (persisted)
        daily_stats = self.email_manager.get_daily_stats()

        # Get total stats from email manager
        email_stats = self.email_manager.get_stats()

        self.logger.info("=" * 100)
        self.logger.info(f"DAILY SUMMARY - {daily_stats['date']}")
        self.logger.info("=" * 100)
        self.logger.info(f"Runtime: {hours}h {minutes}m")
        self.logger.info(f"Emails sent today: {daily_stats['sent_today']}")
        self.logger.info(f"Emails failed today: {daily_stats['failed_today']}")
        self.logger.info(f"Daily limit: {self.daily_limit}")
        self.logger.info(f"Remaining today: {self.daily_limit - daily_stats['sent_today']}")
        self.logger.info("-" * 100)
        self.logger.info(f"Total emails collected: {email_stats['total_collected']}")
        self.logger.info(f"Total emails sent (all time): {email_stats['total_sent']}")
        self.logger.info(f"Total emails failed (all time): {email_stats['total_failed']}")
        self.logger.info(f"Total emails unsent: {email_stats['unsent']}")
        self.logger.info("=" * 100)

    def load_config(self):
        """Load configuration from email_config.json"""
        import json
        import os
        
        config_file = 'email_config.json'
        if not os.path.exists(config_file):
            self.logger.error("No email_config.json found. Please run run_free_scraper.py first.")
            return False
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            self.sender_email = config.get('sender_email')
            self.sender_password = config.get('sender_password')
            self.email_subject = config.get('email_subject')
            self.message_content = config.get('message_content')
            
            self.logger.info(f"Configuration loaded: {self.sender_email}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return False
    
    def send_email(self, recipient_email: str) -> tuple[bool, bool]:
        """
        Send email to recipient with random message variation
        Returns: (success, is_daily_limit_error)
        """
        try:
            # Get random message variation (to avoid Gmail spam detection)
            message_data = get_random_message()

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = message_data['subject']

            # Add both plain text and HTML versions
            msg.attach(MIMEText(message_data['plain'], 'plain'))
            msg.attach(MIMEText(message_data['html'], 'html'))

            # Connect to Gmail SMTP
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            self.logger.info(f"Email sent to: {recipient_email}")
            self.last_successful_email_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True, False

        except Exception as e:
            error_str = str(e)

            # Check if it's a daily limit error
            is_daily_limit = 'Daily user sending limit exceeded' in error_str or '5.4.5' in error_str

            if is_daily_limit:
                self.logger.error(f"GMAIL DAILY LIMIT HIT! Last successful email was at: {self.last_successful_email_time}")
            else:
                self.logger.error(f"Failed to send to {recipient_email}: {e}")

            return False, is_daily_limit
    
    def run(self):
        """Main loop - send emails"""
        # Check if day changed and log summary
        self._check_and_log_daily_summary()

        self.logger.info("=" * 80)
        self.logger.info("SIMPLE EMAIL SENDER")
        self.logger.info("=" * 80)

        # Load configuration
        if not self.load_config():
            return

        # RELOAD email manager data to get latest emails
        self.email_manager = SimpleEmailManager()

        # First, wait until configured start time in configured timezone (if before start time)
        self._wait_until_start_time()

        # Then check if we're in 24h wait period (after start time check)
        can_send, wait_msg = self.email_manager.can_send_emails()
        if not can_send:
            self.logger.warning(f"WAITING FOR 24H PERIOD: {wait_msg}")
            return

        # Get stats
        stats = self.email_manager.get_stats()
        daily_stats = self.email_manager.get_daily_stats()  # Get persisted daily tracking

        self.logger.info(f"Total emails collected: {stats['total_collected']}")
        self.logger.info(f"Already sent: {stats['total_sent']}")
        self.logger.info(f"Failed: {stats['total_failed']}")
        self.logger.info(f"Unsent: {stats['unsent']}")
        self.logger.info(f"Daily limit: {self.daily_limit} emails")
        self.logger.info(f"Sent today so far: {daily_stats['sent_today']}")
        self.logger.info(f"Remaining today: {self.daily_limit - daily_stats['sent_today']}")
        self.logger.info("=" * 80)

        if stats['unsent'] == 0:
            # Check if scraper is complete
            if self._is_scraper_complete():
                self.logger.info("=" * 80)
                self.logger.info("✅ ALL EMAILS SENT AND SCRAPER COMPLETE!")
                self.logger.info("=" * 80)
                self.logger.info(f"Total emails collected: {stats['total_collected']}")
                self.logger.info(f"Total emails sent: {stats['total_sent']}")
                self.logger.info(f"Total emails failed: {stats['total_failed']}")
                self.logger.info("=" * 80)
                self.logger.info("Exiting email sender...")
                exit(0)
            else:
                self.logger.info("No unsent emails. Waiting for scraper to collect more...")
                return

        # Calculate how many we can send today
        remaining_today = self.daily_limit - daily_stats['sent_today']
        if remaining_today <= 0:
            self.logger.info(f"Daily limit already reached ({self.daily_limit}). Waiting for next day...")
            return

        # Get unsent emails (limit to remaining today)
        unsent_emails = self.email_manager.get_unsent_emails(limit=remaining_today)
        self.logger.info(f"Sending to {len(unsent_emails)} emails...")

        sent_count = 0
        failed_count = 0

        for email in unsent_emails:
            # Reload daily stats to check current limit (in case another process updated it)
            daily_stats = self.email_manager.get_daily_stats()

            # Check daily limit
            if daily_stats['sent_today'] >= self.daily_limit:
                self.logger.info(f"Daily limit reached ({self.daily_limit}). Stopping.")
                break

            # Send email
            success, is_daily_limit_error = self.send_email(email)

            # If we hit Gmail's daily limit, stop immediately
            if is_daily_limit_error:
                # Get the last successful email time (from current session or from data)
                last_success_time = self.last_successful_email_time
                if not last_success_time:
                    last_success_time = self.email_manager.get_last_successful_email_time()

                self.logger.error("=" * 80)
                self.logger.error("GMAIL DAILY LIMIT EXCEEDED!")
                self.logger.error(f"Successfully sent {sent_count} emails in this session")
                self.logger.error(f"Last successful email (from data): {last_success_time}")
                self.logger.error("Setting 24-hour wait period from last successful email...")
                self.logger.error("=" * 80)

                # Mark as failed (not sent)
                self.email_manager.mark_as_sent(email, False)

                # Set the 24h wait period from last successful email
                self.email_manager.set_daily_limit_hit(last_success_time)

                # Show when we can resume
                _, wait_msg = self.email_manager.can_send_emails()
                self.logger.error(f"Will resume sending: {wait_msg}")
                break

            # Mark as sent/failed (this also updates daily tracking on disk)
            self.email_manager.mark_as_sent(email, success)

            if success:
                sent_count += 1
            else:
                failed_count += 1

            # Show progress
            if (sent_count + failed_count) % 10 == 0:
                # Reload to show current daily stats
                daily_stats = self.email_manager.get_daily_stats()
                self.logger.info(f"Progress: {sent_count} sent, {failed_count} failed | Today: {daily_stats['sent_today']}/{self.daily_limit}")

            # Delay between emails
            time.sleep(self.delay_between_emails)

        # Final stats (reload to get latest)
        daily_stats = self.email_manager.get_daily_stats()
        self.logger.info("=" * 80)
        self.logger.info(f"SESSION COMPLETED: {sent_count} sent, {failed_count} failed")
        self.logger.info(f"TODAY TOTAL: {daily_stats['sent_today']} sent, {daily_stats['failed_today']} failed")
        self.logger.info(f"REMAINING TODAY: {self.daily_limit - daily_stats['sent_today']} emails")
        self.logger.info("=" * 80)


def main():
    """Main function"""
    sender = SimpleEmailSender()

    try:
        while True:
            sender.run()

            # Wait before checking for new emails (1 minute)
            time.sleep(60)

    except KeyboardInterrupt:
        print("\nStopped by user")


if __name__ == '__main__':
    main()

