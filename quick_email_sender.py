#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Email Sender - Simple wrapper for email_sender.py
"""

import os
import sys

# Fix console encoding for Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    """Quick start for email sender"""
    
    print("\n" + "="*80)
    print("GMAPS EMAIL SENDER - QUICK START".center(80))
    print("="*80 + "\n")
    
    print("Choose an option:\n")
    print("1️⃣  Run Email Sender Only")
    print("   └─ Send emails from already scraped data\n")
    
    print("2️⃣  Run Scraper + Email Sender (Parallel)")
    print("   └─ Scrape emails AND send them simultaneously\n")
    
    print("3️⃣  View Email Sending Status")
    print("   └─ Check how many emails have been sent\n")
    
    print("4️⃣  Reset Email Tracking")
    print("   └─ Clear all tracking data (start fresh)\n")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Email Sender...\n")
        from email_sender import EmailSender
        sender = EmailSender()
        sender.run()
    
    elif choice == "2":
        print("\n🚀 Starting Scraper + Email Sender (Parallel)...\n")
        import run_scraper_and_sender
        run_scraper_and_sender.main()
    
    elif choice == "3":
        print("\n📊 Email Sending Status\n")
        from email_sender import EmailSender
        sender = EmailSender()
        sender.load_tracking_data()
        sender.display_status()
    
    elif choice == "4":
        confirm = input("\n⚠️  Are you sure you want to reset all tracking data? (yes/no): ").strip().lower()
        if confirm == "yes":
            import json
            data = {
                'last_date': '',
                'sent_today': 0,
                'total_sent': 0,
                'failed_count': 0,
                'sent_emails': []
            }
            with open('email_sent_tracking.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ Tracking data reset successfully!")
        else:
            print("❌ Reset cancelled")
    
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Program stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

