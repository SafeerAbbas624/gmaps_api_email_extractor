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
import json

# Set up logging - only to file, not to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("parallel_runner.log", encoding='utf-8')
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
║            GMAPS SCRAPER + EMAIL SENDER PARALLEL RUNNER                    ║
║                                                                            ║
║         Run Google Maps Scraper and Email Sender Simultaneously            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

FEATURES:
  * Run scraper and email sender in parallel
  * Independent thread management
  * Real-time status monitoring
  * Comprehensive logging
  * Easy process control
  * Synchronized operations
  * Error handling for both processes

HOW IT WORKS:
  1. Scraper runs in Thread 1 - Scrapes emails from Google Maps
  2. Email Sender runs in Thread 2 - Sends emails from scraped data
  3. Both processes run simultaneously
  4. Sender reads from scraper's output file
  5. Automatic synchronization

DEVELOPER INFO:
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
        print("\n[PROCESS 1] Starting Google Maps Scraper...")

        # Run scraper as a subprocess to avoid signal handler issues
        result = subprocess.run(
            [sys.executable, "-c",
             "from main import main; main()"],
            cwd=os.getcwd(),
            capture_output=False
        )

        if result.returncode == 0:
            logger.info("Google Maps Scraper completed successfully")
            print("[PROCESS 1] [OK] Google Maps Scraper completed")
        else:
            logger.error(f"Google Maps Scraper exited with code {result.returncode}")
            print(f"[PROCESS 1] [WARNING] Scraper exited with code {result.returncode}")

    except Exception as e:
        logger.error(f"Error in scraper process: {e}")
        print(f"[PROCESS 1] [ERROR] Error: {e}")


def run_email_sender_process():
    """Run the email sender in a separate process"""
    try:
        # Wait a bit for scraper to start and create output file
        print("\n[PROCESS 2] [WAIT] Waiting for scraper to initialize...")
        time.sleep(5)

        logger.info("Starting Email Sender in Process 2...")
        print("[PROCESS 2] Starting Email Sender...")
        print("[PROCESS 2] [PAUSE] Scraper logs will be paused while you enter configuration...")

        # Run email sender as a subprocess
        result = subprocess.run(
            [sys.executable, "-c",
             "from email_sender import EmailSender; sender = EmailSender(); sender.run()"],
            cwd=os.getcwd(),
            capture_output=False
        )

        if result.returncode == 0:
            logger.info("Email Sender completed successfully")
            print("[PROCESS 2] [OK] Email Sender completed")
        else:
            logger.error(f"Email Sender exited with code {result.returncode}")
            print(f"[PROCESS 2] [WARNING] Email Sender exited with code {result.returncode}")

    except Exception as e:
        logger.error(f"Error in email sender process: {e}")
        print(f"[PROCESS 2] [ERROR] Error: {e}")


def main():
    """Main function to run both processes in parallel"""
    display_banner()

    print("\n" + "="*80)
    print("PARALLEL EXECUTION MODE".center(80))
    print("="*80 + "\n")

    print("Process Information:")
    print("  • Process 1: Email Sender (configure first)")
    print("  • Process 2: Google Maps Scraper (starts after config)")
    print("  • Both processes run simultaneously after configuration")
    print("  • Sender reads from scraper's output file")
    print("  • Using subprocess for proper signal handling")
    print("\n" + "="*80 + "\n")

    # Create processes using subprocess
    print("Starting parallel execution...\n")
    print("[WAIT] Starting Email Sender first for configuration...\n")
    print("[IMPORTANT] Please complete email configuration before scraper starts\n")

    scraper_process = None
    sender_process = None
    config_signal_file = ".email_config_done"

    # Remove old signal file if it exists
    if os.path.exists(config_signal_file):
        os.remove(config_signal_file)

    try:
        # Start email sender process FIRST (so user can configure without scraper logs)
        sender_process = subprocess.Popen(
            [sys.executable, "-c",
             "from email_sender import EmailSender; sender = EmailSender(); sender.run()"],
            cwd=os.getcwd()
        )

        # Wait for email configuration to complete (signal file will be created)
        print("[MAIN] [WAIT] Waiting for email configuration to complete...")
        config_timeout = 300  # 5 minutes timeout
        config_start = time.time()

        while not os.path.exists(config_signal_file):
            if time.time() - config_start > config_timeout:
                print("[MAIN] [WARNING] Configuration timeout!")
                break
            time.sleep(0.5)

        print("[MAIN] [OK] Email configuration complete!\n")
        print("[MAIN] Starting Google Maps Scraper in background...\n")

        # Now start scraper process AFTER email sender is configured
        scraper_process = subprocess.Popen(
            [sys.executable, "-c", "from main import main; main()"],
            cwd=os.getcwd()
        )

        # Wait for scraper to complete (sender will continue monitoring)
        scraper_process.wait()

        # Wait for sender to complete (it will stop after no new emails)
        sender_process.wait()

        print("\n" + "="*80)
        print("[OK] ALL PROCESSES COMPLETED SUCCESSFULLY".center(80))
        print("="*80 + "\n")
        logger.info("All processes completed successfully")

        # Clean up signal file
        if os.path.exists(config_signal_file):
            os.remove(config_signal_file)

    except KeyboardInterrupt:
        print("\n\n[STOP] Parallel execution stopped by user")
        logger.info("Parallel execution stopped by user")

        # Terminate both processes
        try:
            if sender_process:
                sender_process.terminate()
            if scraper_process:
                scraper_process.terminate()
            time.sleep(1)
            if sender_process:
                sender_process.kill()
            if scraper_process:
                scraper_process.kill()
        except:
            pass

        # Clean up signal file
        if os.path.exists(config_signal_file):
            os.remove(config_signal_file)

    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"[ERROR] Error: {e}")

        # Clean up signal file
        if os.path.exists(config_signal_file):
            os.remove(config_signal_file)


if __name__ == "__main__":
    main()

