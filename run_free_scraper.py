"""
Main runner for FREE Google Maps Scraper + Email Sender
Runs scraper and email sender in parallel
"""

import subprocess
import sys
import time
import logging
import json
import os
from datetime import datetime
from bot_settings import BotSettingsManager


def setup_logging():
    """Setup logging"""
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/runner.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('runner')


def get_bot_settings():
    """Get or configure bot settings"""
    settings_manager = BotSettingsManager()

    print("\n" + "=" * 80)
    print("BOT SETTINGS CONFIGURATION".center(80))
    print("=" * 80 + "\n")

    # Display current settings
    settings_manager.display_settings()

    # Ask if user wants to change settings
    change_settings = input("Do you want to change any settings? (y/n): ").strip().lower()

    if change_settings == 'y':
        print("\nWhat would you like to change?")
        print("1. Email sending start time")
        print("2. Daily email limit")
        print("3. Delay between emails")
        print("4. Reset all to defaults")
        print("5. Keep current settings")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            current_time = settings_manager.get_start_time()
            current_tz = settings_manager.get_timezone()
            tz_display = current_tz.replace('_', ' ').replace('America/', '').replace('Europe/', '').replace('Asia/', '')
            print(f"\nCurrent start time: {current_time} ({tz_display} Time)")
            new_time = input("Enter new start time (HH:MM in 24-hour format, e.g., 09:00): ").strip()
            if settings_manager.set_start_time(new_time):
                print(f"✓ Start time changed to {new_time}")
            else:
                print("✗ Invalid time format. Using current setting.")

        elif choice == '2':
            current_limit = settings_manager.get_daily_limit()
            print(f"\nCurrent daily limit: {current_limit} emails")
            try:
                new_limit = int(input("Enter new daily limit (positive number): ").strip())
                if settings_manager.set_daily_limit(new_limit):
                    print(f"✓ Daily limit changed to {new_limit}")
                else:
                    print("✗ Invalid limit. Using current setting.")
            except ValueError:
                print("✗ Invalid number. Using current setting.")

        elif choice == '3':
            current_delay = settings_manager.get_delay_between_emails()
            print(f"\nCurrent delay: {current_delay} seconds")
            try:
                new_delay = int(input("Enter new delay in seconds (e.g., 600 for 10 minutes): ").strip())
                if settings_manager.set_delay_between_emails(new_delay):
                    print(f"✓ Delay changed to {new_delay} seconds")
                else:
                    print("✗ Invalid delay. Using current setting.")
            except ValueError:
                print("✗ Invalid number. Using current setting.")

        elif choice == '4':
            confirm = input("Are you sure you want to reset all settings to defaults? (y/n): ").strip().lower()
            if confirm == 'y':
                settings_manager.reset_to_defaults()
                print("✓ All settings reset to defaults")

        # Reload settings after changes
        settings_manager = BotSettingsManager()

    print("\nFinal settings:")
    settings_manager.display_settings()

    return settings_manager


def get_email_config():
    """Get email configuration from user and save to file"""
    config_file = 'email_config.json'

    # Check if config already exists
    if os.path.exists(config_file):
        print("\nFound existing email configuration.")
        use_existing = input("Use existing config? (y/n): ").strip().lower()
        if use_existing == 'y':
            with open(config_file, 'r') as f:
                config = json.load(f)
            print("Using existing email configuration.")
            return config

    print("\n" + "="*80)
    print("EMAIL CONFIGURATION".center(80))
    print("="*80 + "\n")

    # Get sender email
    sender_email = input("Enter your Gmail address: ").strip()
    if not sender_email:
        print("ERROR: Email cannot be empty!")
        return None

    # Get sender password
    sender_password = input("Enter your Gmail App Password: ").strip()
    if not sender_password:
        print("ERROR: Password cannot be empty!")
        return None

    # Get email subject
    default_subject = "Collaborazione autista Londra"
    print(f"\nEmail Subject (default: '{default_subject}'):")
    print("Press Enter to use default, or type a custom subject:")
    custom_subject = input("  > ").strip()
    email_subject = custom_subject if custom_subject else default_subject

    # Get email message
    print("\nEnter the message to send (press Enter twice when done):")
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

    message_content = "\n".join(lines)

    if not message_content.strip():
        print("ERROR: Message cannot be empty!")
        return None

    # Save configuration
    config = {
        'sender_email': sender_email,
        'sender_password': sender_password,
        'email_subject': email_subject,
        'message_content': message_content
    }

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print("\nConfiguration saved!")
    return config


def run_scraper():
    """Run the FREE scraper"""
    logger = logging.getLogger('runner')
    logger.info("Starting FREE Google Maps Scraper...")

    try:
        # Don't capture output - let it display in terminal
        process = subprocess.Popen(
            [sys.executable, 'seleniumbase_scraper.py']
        )

        return process

    except Exception as e:
        logger.error(f"Error starting scraper: {e}")
        return None


def run_email_sender():
    """Run the email sender"""
    logger = logging.getLogger('runner')
    logger.info("Starting Email Sender...")

    try:
        # Use NEW simple email sender (filters "nan" and duplicates)
        process = subprocess.Popen(
            [sys.executable, 'simple_email_sender.py']
        )

        return process

    except Exception as e:
        logger.error(f"Error starting email sender: {e}")
        return None


def main():
    """Main function"""
    logger = setup_logging()

    print("=" * 80)
    print("FREE GOOGLE MAPS SCRAPER + EMAIL SENDER")
    print("=" * 80)
    print("100% FREE - No API costs")
    print("SeleniumBase UC Mode - Undetected by Google")
    print("Rate Limited - 10 req/min, 5000 req/day")
    print("Email Sender - 400 emails/day (with 24h auto-wait on Gmail limit)")
    print("NEW: One file (emails.json) - No duplicates - No 'nan' errors")
    print("Detailed logs: logs/scraper.log & logs/email_sender.log")
    print("=" * 80)
    print()

    # Get bot settings first
    print("\nStep 1: Bot Settings Configuration")
    print("-" * 80)
    settings_manager = get_bot_settings()

    # Get email configuration
    print("\nStep 2: Email Configuration")
    print("-" * 80)
    config = get_email_config()
    if not config:
        logger.error("Failed to get email configuration")
        return

    print("\nStep 3: Starting Processes")
    print("-" * 80)

    # Start scraper
    scraper_process = run_scraper()
    if not scraper_process:
        logger.error("Failed to start scraper")
        return

    # Wait a bit before starting email sender
    time.sleep(5)

    # Start email sender
    sender_process = run_email_sender()
    if not sender_process:
        logger.error("Failed to start email sender")
        scraper_process.terminate()
        return

    logger.info("Both processes started successfully")
    logger.info("Monitoring processes...")
    print("\nBoth processes are running!")
    print("- Scraper: Collecting businesses and emails from Google Maps")
    print("- Email Sender: Sending emails to UNIQUE addresses (no 'nan', no duplicates)")
    print("- Email File: emails.json (all emails in one place)")
    print("\nPress Ctrl+C to stop both processes")
    print("=" * 80)
    
    try:
        # Monitor both processes
        scraper_finished = False
        while True:
            # Check if scraper is still running
            scraper_status = scraper_process.poll()
            sender_status = sender_process.poll()

            if scraper_status is not None and not scraper_finished:
                logger.info(f"Scraper finished with code: {scraper_status}")
                logger.info("Waiting for email sender to complete all remaining emails...")
                scraper_finished = True
                # Don't break - let sender continue until all emails sent

            if sender_status is not None:
                if scraper_finished:
                    # Sender exited after scraper finished - this is expected
                    logger.info(f"Email sender finished with code: {sender_status}")
                    logger.info("All processes completed successfully!")
                    break
                else:
                    # Sender crashed before scraper finished - restart it
                    logger.warning(f"Email sender stopped with code: {sender_status}")
                    logger.info("Restarting email sender...")
                    sender_process = run_email_sender()

            time.sleep(10)  # Check every 10 seconds

    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Stopping processes...")
        scraper_process.terminate()
        sender_process.terminate()

    finally:
        # Wait for processes to finish
        scraper_process.wait()
        sender_process.wait()

        logger.info("=" * 80)
        logger.info("ALL PROCESSES STOPPED")
        logger.info("=" * 80)


if __name__ == "__main__":
    main()

