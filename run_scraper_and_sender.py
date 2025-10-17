#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🚀 GMAPS SCRAPER + EMAIL SENDER PARALLEL RUNNER 🚀             ║
║                                                                            ║
║         Run Google Maps Scraper and Email Sender Simultaneously            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Author: Safeer Abbas
Email: safeerabbas.624@gmail.com
WhatsApp: +923312378492
"""

import threading
import time
import sys
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("parallel_runner.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ParallelRunner")

# Fix console encoding for Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def display_banner():
    """Display beautiful ASCII art banner"""
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🚀 GMAPS SCRAPER + EMAIL SENDER PARALLEL RUNNER 🚀             ║
║                                                                            ║
║         Run Google Maps Scraper and Email Sender Simultaneously            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

✨ FEATURES:
  ✓ Run scraper and email sender in parallel
  ✓ Independent thread management
  ✓ Real-time status monitoring
  ✓ Comprehensive logging
  ✓ Easy process control
  ✓ Synchronized operations
  ✓ Error handling for both processes

⚙️  HOW IT WORKS:
  1. Scraper runs in Thread 1 - Scrapes emails from Google Maps
  2. Email Sender runs in Thread 2 - Sends emails from scraped data
  3. Both processes run simultaneously
  4. Sender reads from scraper's output file
  5. Automatic synchronization

📊 DEVELOPER INFO:
  Name: Safeer Abbas
  Email: safeerabbas.624@gmail.com
  WhatsApp: +923312378492

════════════════════════════════════════════════════════════════════════════
"""
    print(banner)
    logger.info("Parallel Runner started")


def run_scraper():
    """Run the Google Maps scraper"""
    try:
        logger.info("Starting Google Maps Scraper in Thread 1...")
        print("\n[THREAD 1] 🔍 Starting Google Maps Scraper...")
        
        # Import and run the scraper
        from main import main as scraper_main
        scraper_main()
        
        logger.info("Google Maps Scraper completed")
        print("[THREAD 1] ✅ Google Maps Scraper completed")
    
    except Exception as e:
        logger.error(f"Error in scraper thread: {e}")
        print(f"[THREAD 1] ❌ Error: {e}")


def run_email_sender():
    """Run the email sender"""
    try:
        # Wait a bit for scraper to start and create output file
        print("\n[THREAD 2] ⏳ Waiting for scraper to initialize...")
        time.sleep(5)
        
        logger.info("Starting Email Sender in Thread 2...")
        print("[THREAD 2] 📧 Starting Email Sender...")
        
        # Import and run the email sender
        from email_sender import EmailSender
        sender = EmailSender()
        sender.run()
        
        logger.info("Email Sender completed")
        print("[THREAD 2] ✅ Email Sender completed")
    
    except Exception as e:
        logger.error(f"Error in email sender thread: {e}")
        print(f"[THREAD 2] ❌ Error: {e}")


def main():
    """Main function to run both processes in parallel"""
    display_banner()
    
    print("\n" + "="*80)
    print("PARALLEL EXECUTION MODE".center(80))
    print("="*80 + "\n")
    
    print("📋 Process Information:")
    print("  • Thread 1: Google Maps Scraper (scrapes emails)")
    print("  • Thread 2: Email Sender (sends emails)")
    print("  • Both processes run simultaneously")
    print("  • Sender reads from scraper's output file")
    print("\n" + "="*80 + "\n")
    
    # Create threads
    scraper_thread = threading.Thread(target=run_scraper, name="ScraperThread", daemon=False)
    sender_thread = threading.Thread(target=run_email_sender, name="EmailSenderThread", daemon=False)
    
    # Start threads
    print("🚀 Starting parallel execution...\n")
    scraper_thread.start()
    sender_thread.start()
    
    try:
        # Wait for both threads to complete
        scraper_thread.join()
        sender_thread.join()
        
        print("\n" + "="*80)
        print("✅ ALL PROCESSES COMPLETED SUCCESSFULLY".center(80))
        print("="*80 + "\n")
        logger.info("All processes completed successfully")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Parallel execution stopped by user")
        logger.info("Parallel execution stopped by user")
    
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

