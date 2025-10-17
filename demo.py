"""
Demo script for Google Maps Scraper
Shows basic functionality without requiring API key
"""

import os
import pandas as pd
from datetime import datetime

def create_demo_data():
    """Create demo scraped data to show the system working"""
    
    # Sample scraped data (what the scraper would produce)
    demo_data = [
        {
            "name": "ABC Roofing Company",
            "niche": "roofers",
            "address": "123 Main St, San Diego, CA 92101",
            "state": "CA",
            "phone_number": "(619) 555-0123",
            "website": "https://abcroofing.com",
            "result_url": "https://maps.google.com/maps/place/ABC+Roofing"
        },
        {
            "name": "Quick Fix Plumbing",
            "niche": "plumbers", 
            "address": "456 Oak Ave, Los Angeles, CA 90210",
            "state": "CA",
            "phone_number": "(323) 555-0456",
            "website": "https://quickfixplumbing.com",
            "result_url": "https://maps.google.com/maps/place/Quick+Fix+Plumbing"
        },
        {
            "name": "Elite Electricians",
            "niche": "electricians",
            "address": "789 Pine St, San Francisco, CA 94102",
            "state": "CA", 
            "phone_number": "(415) 555-0789",
            "website": "NOT AVAILABLE",
            "result_url": "https://maps.google.com/maps/place/Elite+Electricians"
        },
        {
            "name": "ABC Roofing Company",  # Duplicate
            "niche": "roofers",
            "address": "123 Main St, San Diego, CA 92101", 
            "state": "CA",
            "phone_number": "(619) 555-0123",  # Same phone = duplicate
            "website": "https://abcroofing.com",
            "result_url": "https://maps.google.com/maps/place/ABC+Roofing"
        },
        {
            "name": "Green Landscaping",
            "niche": "landscapers",
            "address": "321 Elm St, Phoenix, AZ 85001",
            "state": "AZ",
            "phone_number": "NOT AVAILABLE",
            "website": "NOT AVAILABLE", 
            "result_url": "https://maps.google.com/maps/place/Green+Landscaping"
        },
        {
            "name": "Desert Landscaping", 
            "niche": "landscapers",
            "address": "654 Cedar Ave, Phoenix, AZ 85002",
            "state": "AZ",
            "phone_number": "NOT AVAILABLE",  # Different business, no phone
            "website": "https://desertlandscaping.com",
            "result_url": "https://maps.google.com/maps/place/Desert+Landscaping"
        }
    ]
    
    return demo_data

def demo_scraper_functionality():
    """Demonstrate the scraper functionality"""
    print("Google Maps Scraper - Demo")
    print("=" * 40)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Create demo data
    demo_data = create_demo_data()
    
    print(f"📊 Created {len(demo_data)} sample records")
    print("\nSample data:")
    for i, record in enumerate(demo_data[:2], 1):
        print(f"\n{i}. {record['name']}")
        print(f"   Niche: {record['niche']}")
        print(f"   Address: {record['address']}")
        print(f"   Phone: {record['phone_number']}")
        print(f"   Website: {record['website']}")
    
    # Save raw data
    df = pd.DataFrame(demo_data)
    raw_file = "output/demo_raw_data.csv"
    df.to_csv(raw_file, index=False)
    print(f"\n💾 Saved raw data to: {raw_file}")
    
    # Demonstrate duplicate removal
    print("\n🔍 Removing duplicates...")
    
    # Remove duplicates based on phone number
    df_with_phone = df[df['phone_number'] != 'NOT AVAILABLE'].drop_duplicates(subset=['phone_number'])
    df_no_phone = df[df['phone_number'] == 'NOT AVAILABLE']
    clean_df = pd.concat([df_with_phone, df_no_phone], ignore_index=True)
    
    # Save clean data
    clean_file = "output/demo_clean_data.csv"
    clean_df.to_csv(clean_file, index=False)
    
    removed_count = len(df) - len(clean_df)
    print(f"✅ Removed {removed_count} duplicates")
    print(f"📊 Final data: {len(clean_df)} unique records")
    print(f"💾 Saved clean data to: {clean_file}")
    
    # Show statistics
    print("\n📈 Data Statistics:")
    print(f"   Total records: {len(clean_df)}")
    print(f"   Unique niches: {len(clean_df['niche'].unique())}")
    print(f"   Unique states: {len(clean_df['state'].unique())}")
    print(f"   Records with phone: {len(clean_df[clean_df['phone_number'] != 'NOT AVAILABLE'])}")
    print(f"   Records with website: {len(clean_df[clean_df['website'] != 'NOT AVAILABLE'])}")
    
    print("\n🎯 Niches found:")
    for niche in clean_df['niche'].unique():
        count = len(clean_df[clean_df['niche'] == niche])
        print(f"   {niche}: {count} businesses")
    
    print("\n🗺️  States covered:")
    for state in clean_df['state'].unique():
        count = len(clean_df[clean_df['state'] == state])
        print(f"   {state}: {count} businesses")
    
    print("\n" + "=" * 40)
    print("Demo completed successfully!")
    print("\nTo use with real data:")
    print("1. Get a Google Maps API key")
    print("2. Add it to .env file")
    print("3. Run: python main.py --mode single --niche 'roofers' --location 'San Diego, CA'")
    print("4. For continuous: python main.py --mode continuous")

if __name__ == "__main__":
    demo_scraper_functionality()
