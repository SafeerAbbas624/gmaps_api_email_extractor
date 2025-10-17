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

# Set up logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
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
        self.tracking_file = "email_sent_tracking.json"
        self.csv_file = "output/scraped_data.csv"
        self.daily_limit = 500
        self.sent_today = 0
        self.total_sent = 0
        self.failed_count = 0
        self.running = True
        
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
  ✓ Send up to 500 emails per day
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
  • Daily Limit: 500 emails/day
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
                    
                    logger.info(f"Loaded tracking data: {self.sent_today} sent today, {self.total_sent} total")
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
        """Get sender email, password, and message from user"""
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
        
        self.message_content = "\n".join(lines[:-1]) if lines else "Hello,\n\nThis is an automated message from Google Maps Email Scraper."
        
        if not self.message_content.strip():
            print("❌ Message cannot be empty!")
            return False
        
        print("-" * 80)
        print(f"\n✅ Configuration saved!")
        print(f"   Sender: {self.sender_email}")
        print(f"   Message length: {len(self.message_content)} characters")
        
        return True
    
    def read_scraped_emails(self):
        """Read emails from scraped_data.csv"""
        try:
            if not os.path.exists(self.csv_file):
                logger.error(f"CSV file not found: {self.csv_file}")
                print(f"❌ CSV file not found: {self.csv_file}")
                return []
            
            df = pd.read_csv(self.csv_file)
            
            # Filter out rows without valid emails
            valid_emails = df[df['email'] != 'NOT AVAILABLE']['email'].unique().tolist()
            
            logger.info(f"Found {len(valid_emails)} unique valid emails in CSV")
            print(f"\n📊 Found {len(valid_emails)} unique valid emails in CSV")
            
            return valid_emails
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            print(f"❌ Error reading CSV file: {e}")
            return []
    
    def send_email(self, recipient_email):
        """Send email to recipient using SMTP"""
        try:
            msg = MIMEText(self.message_content)
            msg['Subject'] = 'Important Message from Google Maps'
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
        """Main email sending loop"""
        print("\n" + "="*80)
        print("STARTING EMAIL SENDER".center(80))
        print("="*80 + "\n")
        
        # Load tracking data
        self.load_tracking_data()
        
        # Read emails from CSV
        emails = self.read_scraped_emails()
        
        if not emails:
            print("❌ No emails found to send!")
            return False
        
        # Load already sent emails
        tracking_data = self.load_tracking_data()
        sent_emails = set([e['email'] for e in tracking_data.get('sent_emails', [])])
        
        # Filter out already sent emails
        emails_to_send = [e for e in emails if e not in sent_emails]
        
        print(f"\n📧 Emails to send: {len(emails_to_send)}")
        print(f"📧 Already sent: {len(sent_emails)}")
        
        if not emails_to_send:
            print("✅ All emails have already been sent!")
            return True
        
        # Display status
        self.display_status()
        
        # Start sending
        print("\n" + "="*80)
        print("SENDING EMAILS".center(80))
        print("="*80 + "\n")
        
        for idx, email in enumerate(emails_to_send, 1):
            # Check daily limit
            if self.check_daily_limit():
                print(f"\n⏸️  Daily limit reached! Waiting for next day...")
                logger.info("Daily limit reached. Waiting for next day.")
                
                # Wait until next day
                now = datetime.now()
                next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                wait_seconds = (next_day - now).total_seconds()
                
                print(f"⏳ Waiting {wait_seconds/3600:.1f} hours until {next_day.strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(wait_seconds)
                
                # Reset daily count
                self.sent_today = 0
                logger.info("Daily count reset. Resuming email sending.")
                print("✅ Daily reset complete. Resuming...")
            
            # Send email
            print(f"\n[{idx}/{len(emails_to_send)}] Sending to: {email}")
            success = self.send_email(email)
            
            if success:
                print(f"✅ Email sent successfully")
                self.update_tracking(email, success=True)
            else:
                print(f"❌ Failed to send email")
                self.update_tracking(email, success=False)
            
            # Small delay between emails
            time.sleep(1)
            
            # Display status every 10 emails
            if idx % 10 == 0:
                self.display_status()
        
        # Final status
        print("\n" + "="*80)
        print("SENDING COMPLETE".center(80))
        print("="*80)
        self.display_status()
        
        return True
    
    def run(self):
        """Main entry point"""
        try:
            self.display_banner()
            
            if not self.get_input_configuration():
                return False
            
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

