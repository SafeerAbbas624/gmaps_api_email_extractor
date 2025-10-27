#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    📧 GMAPS EMAIL SENDER v1.0 📧                          ║
║                                                                            ║
║              Automated Email Sender for Google Maps Scraper                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Author: Safeer Abbas
Email: safeerabbas.624@gmail.com
WhatsApp: +923312378492
"""

import smtplib
from email.mime.text import MIMEText
import pandas as pd
import json
import os
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import threading

# Set up logging with UTF-8 encoding (initially disabled for configuration)
logging.basicConfig(
    level=logging.CRITICAL,  # Start with CRITICAL to suppress logs during config
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("email_sender.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("EmailSender")

# Fix console encoding for Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class EmailSender:
    def __init__(self):
        self.sender_email = None
        self.sender_password = None
        self.message_content = None
        self.email_subject = "Collaborazione autista Londra"  # Default subject
        self.tracking_file = "email_sent_tracking.json"
        self.csv_file = "output/scraped_data.csv"
        self.daily_limit = 400  # Changed from 500 to 400 to leave margin for replies
        self.sent_today = 0
        self.total_sent = 0
        self.failed_count = 0
        self.running = True
        self.current_date = datetime.now().strftime('%Y-%m-%d')  # Track current date
        
    def display_banner(self):
        """Display beautiful ASCII art banner"""
        banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    📧 GMAPS EMAIL SENDER v1.0 📧                          ║
║                                                                            ║
║              Automated Email Sender for Google Maps Scraper                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

✨ FEATURES:
  ✓ Send up to 400 emails per day
  ✓ Automatic daily limit reset at midnight
  ✓ Resume from where you left off
  ✓ Beautiful progress display
  ✓ Comprehensive logging
  ✓ Error handling and retry logic
  ✓ Works alongside Google Maps scraper
  ✓ Real-time email tracking
  ✓ Duplicate email prevention
  ✓ Professional email formatting

⚙️  SPECIFICATIONS:
  • Daily Limit: 400 emails/day (100 margin for replies)
  • Email Provider: Gmail SMTP
  • Encoding: UTF-8
  • Logging: Enabled
  • Tracking: JSON-based

📊 DEVELOPER INFO:
  Name: Safeer Abbas
  Email: safeerabbas.624@gmail.com
  WhatsApp: +923312378492

════════════════════════════════════════════════════════════════════════════
"""
        print(banner)
        logger.info("Email Sender started")
    
    def load_tracking_data(self):
        """Load email tracking data from JSON file"""
        try:
            if os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Check if we need to reset daily count
                    last_date = data.get('last_date')
                    today = datetime.now().strftime('%Y-%m-%d')
                    
                    if last_date != today:
                        logger.info(f"Date changed from {last_date} to {today}. Resetting daily count.")
                        data['sent_today'] = 0
                        data['last_date'] = today
                        self.save_tracking_data(data)
                    
                    self.sent_today = data.get('sent_today', 0)
                    self.total_sent = data.get('total_sent', 0)
                    self.failed_count = data.get('failed_count', 0)
                    self.current_date = data.get('last_date', today)  # Update current_date from tracking file

                    logger.info(f"Loaded tracking data: {self.sent_today} sent today, {self.total_sent} total, date: {self.current_date}")
                    return data
            else:
                logger.info("No tracking file found. Creating new one.")
                return self.create_new_tracking_file()
        except Exception as e:
            logger.error(f"Error loading tracking data: {e}")
            return self.create_new_tracking_file()
    
    def create_new_tracking_file(self):
        """Create a new tracking file"""
        data = {
            'last_date': datetime.now().strftime('%Y-%m-%d'),
            'sent_today': 0,
            'total_sent': 0,
            'failed_count': 0,
            'sent_emails': []
        }
        self.save_tracking_data(data)
        return data
    
    def save_tracking_data(self, data):
        """Save tracking data to JSON file"""
        try:
            with open(self.tracking_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("Tracking data saved")
        except Exception as e:
            logger.error(f"Error saving tracking data: {e}")
    
    def get_input_configuration(self):
        """Get sender email, password, subject, and message from user"""
        print("\n" + "="*80)
        print("CONFIGURATION".center(80))
        print("="*80 + "\n")

        # Get sender email
        self.sender_email = input("📧 Enter your Gmail address: ").strip()
        if not self.sender_email:
            print("❌ Email cannot be empty!")
            return False

        # Get sender password
        self.sender_password = input("🔐 Enter your Gmail App Password (or password): ").strip()
        if not self.sender_password:
            print("❌ Password cannot be empty!")
            return False

        # Get email subject with default option
        print(f"\n📌 Email Subject (default: '{self.email_subject}'):")
        print("   Press Enter to use default, or type a custom subject:")
        custom_subject = input("   ➜ ").strip()
        if custom_subject:
            self.email_subject = custom_subject
            print(f"   ✅ Using custom subject: '{self.email_subject}'")
        else:
            print(f"   ✅ Using default subject: '{self.email_subject}'")

        # Get message
        print("\n📝 Enter the message to send (press Enter twice when done):")
        print("-" * 80)
        lines = []
        empty_count = 0
        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)

        # Remove the last empty line that was added before the second Enter
        if lines and lines[-1] == "":
            lines = lines[:-1]

        self.message_content = "\n".join(lines) if lines else "Hello,\n\nThis is an automated message from Google Maps Email Scraper."

        if not self.message_content.strip():
            print("❌ Message cannot be empty!")
            return False

        print("-" * 80)
        print(f"\n✅ Configuration saved!")
        print(f"   Sender: {self.sender_email}")
        print(f"   Subject: {self.email_subject}")
        print(f"   Message length: {len(self.message_content)} characters")

        # Enable logging after configuration is complete
        logging.getLogger().setLevel(logging.INFO)
        logger.info("Configuration completed. Starting email sending...")

        return True
    
    def read_scraped_emails(self):
        """Read emails from scraped_data.csv and temp file"""
        try:
            all_emails = []

            # Read from main CSV file
            if os.path.exists(self.csv_file):
                try:
                    df = pd.read_csv(self.csv_file)
                    valid_emails = df[df['email'] != 'NOT AVAILABLE']['email'].unique().tolist()
                    all_emails.extend(valid_emails)
                except Exception as e:
                    logger.warning(f"Error reading main CSV: {e}")

            # Also read from temp file (for real-time updates)
            temp_file = "output/temp_scraped_data.csv"
            if os.path.exists(temp_file):
                try:
                    df_temp = pd.read_csv(temp_file)
                    valid_emails_temp = df_temp[df_temp['email'] != 'NOT AVAILABLE']['email'].unique().tolist()
                    all_emails.extend(valid_emails_temp)
                except Exception as e:
                    logger.warning(f"Error reading temp CSV: {e}")

            # Remove duplicates while preserving order
            seen = set()
            unique_emails = []
            for email in all_emails:
                if email not in seen:
                    seen.add(email)
                    unique_emails.append(email)

            logger.info(f"Found {len(unique_emails)} unique valid emails in CSV")
            if len(unique_emails) > 0:
                print(f"\n📊 Found {len(unique_emails)} unique valid emails in CSV")

            return unique_emails
        except Exception as e:
            logger.error(f"Error reading CSV files: {e}")
            print(f"❌ Error reading CSV files: {e}")
            return []
    
    def send_email(self, recipient_email):
        """Send email to recipient using SMTP"""
        try:
            msg = MIMEText(self.message_content)
            msg['Subject'] = self.email_subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            # Connect to Gmail SMTP server
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent successfully to {recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error(f"Authentication failed for {self.sender_email}")
            print("❌ Authentication failed! Check your email and password.")
            return False
        except Exception as e:
            logger.error(f"Error sending email to {recipient_email}: {e}")
            return False
    
    def update_tracking(self, email, success=True):
        """Update tracking data after sending email"""
        try:
            data = self.load_tracking_data()
            
            if success:
                self.sent_today += 1
                self.total_sent += 1
                data['sent_emails'].append({
                    'email': email,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success'
                })
            else:
                self.failed_count += 1
                data['sent_emails'].append({
                    'email': email,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'failed'
                })
            
            data['sent_today'] = self.sent_today
            data['total_sent'] = self.total_sent
            data['failed_count'] = self.failed_count
            data['last_date'] = datetime.now().strftime('%Y-%m-%d')
            
            self.save_tracking_data(data)
        except Exception as e:
            logger.error(f"Error updating tracking: {e}")
    
    def check_and_reset_if_new_day(self):
        """Check if it's a new day and reset the counter at midnight"""
        today = datetime.now().strftime('%Y-%m-%d')

        if today != self.current_date:
            logger.info(f"[RESET] Date changed from {self.current_date} to {today}. Resetting daily count at midnight.")
            print(f"\n[MIDNIGHT RESET] New day detected! Resetting counter from {self.sent_today} to 0")

            # Reset the counter
            self.sent_today = 0
            self.current_date = today

            # Update tracking file with new date
            try:
                if os.path.exists(self.tracking_file):
                    with open(self.tracking_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    data['sent_today'] = 0
                    data['last_date'] = today

                    self.save_tracking_data(data)
                    logger.info("[RESET] Tracking file updated with new date and reset counter")
            except Exception as e:
                logger.error(f"Error updating tracking file during reset: {e}")

            return True  # Indicates a reset occurred

        return False  # No reset needed

    def check_daily_limit(self):
        """Check if daily limit has been reached"""
        if self.sent_today >= self.daily_limit:
            logger.warning(f"Daily limit reached: {self.sent_today}/{self.daily_limit}")
            return True
        return False
    
    def display_status(self):
        """Display current sending status"""
        remaining = self.daily_limit - self.sent_today
        percentage = (self.sent_today / self.daily_limit) * 100
        
        status = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                          📊 SENDING STATUS 📊                             ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  Today's Progress:     {self.sent_today:>3}/{self.daily_limit} emails sent ({percentage:>5.1f}%)                    ║
║  Remaining Today:      {remaining:>3} emails                                    ║
║  Total Sent (All):     {self.total_sent:>3} emails                                    ║
║  Failed Attempts:      {self.failed_count:>3} emails                                    ║
║  Last Updated:         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
        print(status)
    
    def start_sending(self):
        """Main email sending loop - continuously monitors CSV for new emails"""
        print("\n" + "="*80)
        print("STARTING EMAIL SENDER".center(80))
        print("="*80 + "\n")

        # Load tracking data
        self.load_tracking_data()

        # Load already sent emails
        tracking_data = self.load_tracking_data()
        sent_emails = set([e['email'] for e in tracking_data.get('sent_emails', [])])

        print(f"📧 Already sent: {len(sent_emails)}")
        print("⏳ Monitoring CSV file for new emails from scraper...\n")

        # Display status
        self.display_status()

        # Start sending
        print("\n" + "="*80)
        print("SENDING EMAILS (CONTINUOUS MONITORING)".center(80))
        print("="*80 + "\n")

        total_sent_this_session = 0

        while True:
            # Check if it's a new day and reset counter at midnight
            self.check_and_reset_if_new_day()

            # Check daily limit
            if self.check_daily_limit():
                print(f"\n⏸️  Daily limit reached ({self.daily_limit} emails)! Waiting for next day...")
                logger.info(f"Daily limit reached ({self.daily_limit} emails). Waiting for next day.")

                # Wait until next day (midnight)
                now = datetime.now()
                next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                wait_seconds = (next_day - now).total_seconds()

                print(f"⏳ Waiting {wait_seconds/3600:.1f} hours until midnight: {next_day.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"Waiting {wait_seconds/3600:.1f} hours until midnight")
                time.sleep(wait_seconds)

                # After waking up at midnight, the next loop iteration will call check_and_reset_if_new_day()
                # which will reset the counter
                logger.info("Woke up at midnight. Next iteration will reset counter.")
                print("✅ Midnight reached. Checking for new day...")
                continue  # Go back to start of loop to trigger reset check

            # Read current emails from CSV
            current_emails = self.read_scraped_emails()

            # Find new emails that haven't been sent
            new_emails = [e for e in current_emails if e not in sent_emails]

            if new_emails:
                # Send the first new email
                email = new_emails[0]
                total_sent_this_session += 1

                print(f"\n[NEW EMAIL] Sending to: {email}")
                success = self.send_email(email)

                if success:
                    print(f"✅ Email sent successfully")
                    self.update_tracking(email, success=True)
                    sent_emails.add(email)
                    logger.info(f"Email sent to {email}. Total this session: {total_sent_this_session}")
                else:
                    print(f"❌ Failed to send email")
                    self.update_tracking(email, success=False)
                    logger.error(f"Failed to send email to {email}")

                # Small delay between emails
                time.sleep(2)

                # Display status every 5 emails
                if total_sent_this_session % 5 == 0:
                    self.display_status()
            else:
                # No new emails found - keep waiting for scraper to find more
                print("⏳ Waiting for scraper to find more emails...", end='\r')
                logger.info("Waiting for new emails from scraper...")

                # Wait before checking again
                time.sleep(5)

        # Final status
        print("\n" + "="*80)
        print("SENDING COMPLETE".center(80))
        print("="*80)
        print(f"\n📊 Emails sent this session: {total_sent_this_session}")
        self.display_status()

        return True
    
    def run(self):
        """Main entry point"""
        try:
            self.display_banner()

            if not self.get_input_configuration():
                return False

            # Create signal file to indicate configuration is complete
            # This allows the parallel runner to start the scraper
            config_signal_file = ".email_config_done"
            try:
                with open(config_signal_file, 'w') as f:
                    f.write("Configuration complete")
                logger.info("Configuration signal file created")
            except Exception as e:
                logger.error(f"Error creating signal file: {e}")

            return self.start_sending()

        except KeyboardInterrupt:
            print("\n\n⏹️  Email sender stopped by user")
            logger.info("Email sender stopped by user")
            return False

        except Exception as e:
            logger.critical(f"Critical error: {e}")
            print(f"❌ Critical error: {e}")
            return False


def main():
    """Main function"""
    sender = EmailSender()
    sender.run()


if __name__ == "__main__":
    main()

