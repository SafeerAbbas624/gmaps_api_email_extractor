"""
Quick Start Script for Google Maps Scraper
Interactive setup and testing
"""

import os
import sys
from dotenv import load_dotenv

def check_setup():
    """Check if the system is properly set up"""
    issues = []
    
    # Check if .env exists
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found. Run: cp .env.example .env")
    
    # Check API key
    load_dotenv()
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        issues.append("❌ Google Maps API key not configured in .env file")
    else:
        print("✅ API key found")
    
    # Check input files
    if not os.path.exists('input/niches.csv'):
        issues.append("❌ input/niches.csv not found")
    else:
        print("✅ Niches file found")
    
    if not os.path.exists('input/locations.csv'):
        issues.append("❌ input/locations.csv not found")
    else:
        print("✅ Locations file found")
    
    # Check dependencies
    try:
        import googlemaps
        import pandas
        print("✅ Dependencies installed")
    except ImportError as e:
        issues.append(f"❌ Missing dependency: {e}")
    
    return issues

def interactive_setup():
    """Interactive setup process"""
    print("Google Maps Scraper - Quick Start")
    print("=" * 40)
    
    # Check current setup
    issues = check_setup()
    
    if issues:
        print("\nSetup Issues Found:")
        for issue in issues:
            print(issue)
        
        print("\nPlease fix these issues and run again.")
        return False
    
    print("\n✅ All checks passed!")
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run a test search")
    print("2. Start continuous scraping")
    print("3. View current progress")
    print("4. Clean existing data")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        run_test_search()
    elif choice == "2":
        start_continuous_scraping()
    elif choice == "3":
        view_progress()
    elif choice == "4":
        clean_data()
    elif choice == "5":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again.")
    
    return True

def run_test_search():
    """Run a test search"""
    print("\nRunning test search...")
    
    niche = input("Enter niche (e.g., 'roofers'): ").strip()
    location = input("Enter location (e.g., 'San Diego, CA'): ").strip()
    
    if not niche or not location:
        print("❌ Both niche and location are required")
        return
    
    print(f"\nTesting: {niche} in {location}")
    print("This may take a few moments...")
    
    try:
        os.system(f'python main.py --mode single --niche "{niche}" --location "{location}"')
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")

def start_continuous_scraping():
    """Start continuous scraping"""
    print("\n⚠️  Starting continuous scraping...")
    print("This will process ALL niches and locations in your input files.")
    print("The scraper will run until completed or manually stopped (Ctrl+C).")
    
    confirm = input("\nDo you want to continue? (y/N): ").strip().lower()
    
    if confirm == 'y':
        print("\nStarting continuous scraping...")
        print("Press Ctrl+C to stop gracefully")
        
        try:
            os.system('python main.py --mode continuous')
        except KeyboardInterrupt:
            print("\n❌ Scraping interrupted by user")
    else:
        print("Continuous scraping cancelled")

def view_progress():
    """View current progress"""
    print("\nCurrent Progress:")
    os.system('python utils.py progress')
    
    print("\nData Statistics:")
    os.system('python utils.py stats')

def clean_data():
    """Clean existing data"""
    print("\nCleaning data (removing duplicates)...")
    os.system('python utils.py clean')

if __name__ == "__main__":
    try:
        interactive_setup()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)
