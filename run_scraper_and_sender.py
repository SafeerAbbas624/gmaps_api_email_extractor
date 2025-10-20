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

import subprocess
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


def run_scraper_process():
    """Run the Google Maps scraper in a separate process"""
    try:
        logger.info("Starting Google Maps Scraper in Process 1...")
        print("\n[PROCESS 1] 🔍 Starting Google Maps Scraper...")

        # Run scraper as a subprocess to avoid signal handler issues
        result = subprocess.run(
            [sys.executable, "-c",
             "from main import main; main()"],
            cwd=os.getcwd(),
            capture_output=False
        )

        if result.returncode == 0:
            logger.info("Google Maps Scraper completed successfully")
            print("[PROCESS 1] ✅ Google Maps Scraper completed")
        else:
            logger.error(f"Google Maps Scraper exited with code {result.returncode}")
            print(f"[PROCESS 1] ⚠️  Scraper exited with code {result.returncode}")

    except Exception as e:
        logger.error(f"Error in scraper process: {e}")
        print(f"[PROCESS 1] ❌ Error: {e}")


def run_email_sender_process():
    """Run the email sender in a separate process"""
    try:
        # Wait a bit for scraper to start and create output file
        print("\n[PROCESS 2] ⏳ Waiting for scraper to initialize...")
        time.sleep(5)

        logger.info("Starting Email Sender in Process 2...")
        print("[PROCESS 2] 📧 Starting Email Sender...")

        # Run email sender as a subprocess
        result = subprocess.run(
            [sys.executable, "-c",
             "from email_sender import EmailSender; sender = EmailSender(); sender.run()"],
            cwd=os.getcwd(),
            capture_output=False
        )

        if result.returncode == 0:
            logger.info("Email Sender completed successfully")
            print("[PROCESS 2] ✅ Email Sender completed")
        else:
            logger.error(f"Email Sender exited with code {result.returncode}")
            print(f"[PROCESS 2] ⚠️  Email Sender exited with code {result.returncode}")

    except Exception as e:
        logger.error(f"Error in email sender process: {e}")
        print(f"[PROCESS 2] ❌ Error: {e}")


def main():
    """Main function to run both processes in parallel"""
    display_banner()

    print("\n" + "="*80)
    print("PARALLEL EXECUTION MODE".center(80))
    print("="*80 + "\n")

    print("📋 Process Information:")
    print("  • Process 1: Google Maps Scraper (scrapes emails)")
    print("  • Process 2: Email Sender (sends emails)")
    print("  • Both processes run simultaneously")
    print("  • Sender reads from scraper's output file")
    print("  • Using subprocess for proper signal handling")
    print("\n" + "="*80 + "\n")

    # Create processes using subprocess
    print("🚀 Starting parallel execution...\n")

    try:
        # Start scraper process
        scraper_process = subprocess.Popen(
            [sys.executable, "-c", "from main import main; main()"],
            cwd=os.getcwd()
        )

        # Start email sender process (with delay)
        time.sleep(5)
        sender_process = subprocess.Popen(
            [sys.executable, "-c", "from email_sender import EmailSender; sender = EmailSender(); sender.run()"],
            cwd=os.getcwd()
        )

        # Wait for both processes to complete
        scraper_process.wait()
        sender_process.wait()

        print("\n" + "="*80)
        print("✅ ALL PROCESSES COMPLETED SUCCESSFULLY".center(80))
        print("="*80 + "\n")
        logger.info("All processes completed successfully")

    except KeyboardInterrupt:
        print("\n\n⏹️  Parallel execution stopped by user")
        logger.info("Parallel execution stopped by user")

        # Terminate both processes
        try:
            scraper_process.terminate()
            sender_process.terminate()
            time.sleep(1)
            scraper_process.kill()
            sender_process.kill()
        except:
            pass

    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

