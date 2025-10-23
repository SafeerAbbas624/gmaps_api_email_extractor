#!/usr/bin/env python3
"""
Quick scraper test - runs for just 2 niches and 2 locations
Tests the full integration of dual API system with scraper
"""

import sys
import os
import csv
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ScraperRunner
from config import config

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def create_test_input_files():
    """Create minimal test input files"""
    print_header("CREATING TEST INPUT FILES")
    
    # Create test niches
    test_niches = [
        "agenzie di viaggio",
        "tour operator"
    ]
    
    with open('input/niches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['niche'])
        for niche in test_niches:
            writer.writerow([niche])
    
    print(f"✅ Created test niches.csv with {len(test_niches)} niches")
    
    # Create test locations
    test_locations = [
        ("Napoli", "Italia"),
        ("Roma", "Italia")
    ]
    
    with open('input/locations.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['city', 'state'])
        for city, state in test_locations:
            writer.writerow([city, state])
    
    print(f"✅ Created test locations.csv with {len(test_locations)} locations")

def check_output_files():
    """Check what was scraped"""
    print_header("CHECKING OUTPUT FILES")
    
    # Check scraped data
    if os.path.exists('output/scraped_data.csv'):
        with open('output/scraped_data.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"✅ output/scraped_data.csv: {len(lines)-1} records (excluding header)")
        
        if len(lines) > 1:
            # Count emails
            with open('output/scraped_data.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                emails_found = sum(1 for row in reader if row.get('email') and row['email'] != 'NOT AVAILABLE')
            
            print(f"   📧 Emails found: {emails_found}")
    else:
        print("❌ output/scraped_data.csv not found")
    
    # Check API usage
    if os.path.exists('output/api_usage.json'):
        with open('output/api_usage.json', 'r', encoding='utf-8') as f:
            usage = json.load(f)
        
        print(f"\n✅ API Usage Statistics:")
        print(f"   API 1 Daily Requests: {usage['api_1']['daily_requests']}")
        print(f"   API 1 Monthly Requests: {usage['api_1']['monthly_requests']}")
        print(f"   API 2 Daily Requests: {usage['api_2']['daily_requests']}")
        print(f"   API 2 Monthly Requests: {usage['api_2']['monthly_requests']}")
        print(f"   Daily Emails: {usage['daily_emails']}")
        print(f"   Current API: {usage.get('current_api', 'N/A')}")
    else:
        print("❌ output/api_usage.json not found")
    
    # Check logs
    if os.path.exists('logs/scraper.log'):
        with open('logs/scraper.log', 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        print(f"\n✅ logs/scraper.log: {len(log_lines)} log entries")
        
        # Show last 10 lines
        print("\n   Last 10 log entries:")
        for line in log_lines[-10:]:
            print(f"   {line.rstrip()}")
    else:
        print("❌ logs/scraper.log not found")

def main():
    """Run quick scraper test"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  QUICK SCRAPER TEST (2 niches x 2 locations)".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        # Create test input files
        create_test_input_files()
        
        # Initialize runner
        print_header("INITIALIZING SCRAPER")
        runner = ScraperRunner()
        runner.initialize()
        print("✅ Scraper initialized successfully")
        
        # Run single search for testing
        print_header("RUNNING QUICK SCRAPE TEST")
        print("Scraping: agenzie di viaggio in Napoli")
        runner.run_single_search("agenzie di viaggio", "Napoli, Italia")
        
        print("\nScraping: tour operator in Roma")
        runner.run_single_search("tour operator", "Roma, Italia")
        
        # Check results
        check_output_files()
        
        print_header("TEST COMPLETE")
        print("✅ Quick scraper test completed successfully!")
        print("\nNext steps:")
        print("1. Check output/scraped_data.csv for scraped data")
        print("2. Check output/api_usage.json for API usage stats")
        print("3. Check logs/scraper.log for detailed logs")
        print("4. Run full scraper with: python run_scraper_and_sender.py")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "█"*70 + "\n")

if __name__ == "__main__":
    main()

