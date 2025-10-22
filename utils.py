"""
Utility functions for Google Maps Scraper
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from config import config


def show_progress():
    """Display current scraping progress"""
    try:
        if not os.path.exists(config.progress_file):
            print("No progress file found. Scraper hasn't been run yet.")
            return
        
        with open(config.progress_file, 'r') as f:
            progress = json.load(f)
        
        print("Current Scraping Progress")
        print("=" * 30)
        print(f"Current niche index: {progress.get('current_niche_index', 0)}")
        print(f"Current location index: {progress.get('current_location_index', 0)}")
        print(f"Total scraped: {progress.get('total_scraped', 0)}")
        print(f"Daily requests: {progress.get('daily_requests', 0)}")
        print(f"Last update: {progress.get('last_update', 'Unknown')}")
        
    except Exception as e:
        print(f"Error reading progress: {e}")


def show_data_stats():
    """Display statistics about scraped data"""
    try:
        if not os.path.exists(config.output_file):
            print("No output file found. No data has been scraped yet.")
            return
        
        df = pd.read_csv(config.output_file)
        
        print("Data Statistics")
        print("=" * 20)
        print(f"Total records: {len(df)}")
        
        if len(df) > 0:
            print(f"Unique phone numbers: {len(df[df['phone_number'] != 'NOT AVAILABLE']['phone_number'].unique())}")
            print(f"Records with phone: {len(df[df['phone_number'] != 'NOT AVAILABLE'])}")
            print(f"Records with website: {len(df[df['website'] != 'NOT AVAILABLE'])}")
            print(f"Unique niches: {len(df['niche'].unique())}")
            print(f"Unique states: {len(df['state'].unique())}")
            
            print("\nTop 5 niches by count:")
            niche_counts = df['niche'].value_counts().head()
            for niche, count in niche_counts.items():
                print(f"  {niche}: {count}")
            
            print("\nTop 5 states by count:")
            state_counts = df['state'].value_counts().head()
            for state, count in state_counts.items():
                print(f"  {state}: {count}")
        
    except Exception as e:
        print(f"Error reading data stats: {e}")


def reset_progress():
    """Reset scraping progress (start from beginning)"""
    try:
        if os.path.exists(config.progress_file):
            os.remove(config.progress_file)
            print("✅ Progress reset. Scraper will start from the beginning.")
        else:
            print("No progress file found.")
    except Exception as e:
        print(f"Error resetting progress: {e}")


def clean_data():
    """Remove duplicates from scraped data"""
    try:
        from data_manager import DataManager
        
        data_manager = DataManager()
        removed_count = data_manager.remove_duplicates_and_finalize()
        
        print(f"✅ Removed {removed_count} duplicates")
        print(f"Clean data saved to: {config.output_file.replace('.csv', '_final.csv')}")
        
    except Exception as e:
        print(f"Error cleaning data: {e}")


def backup_data():
    """Create a manual backup of current data"""
    try:
        if not os.path.exists(config.output_file):
            print("No data file found to backup.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_file = os.path.join(backup_dir, f"manual_backup_{timestamp}.csv")
        
        import shutil
        shutil.copy2(config.output_file, backup_file)
        
        print(f"✅ Backup created: {backup_file}")
        
    except Exception as e:
        print(f"Error creating backup: {e}")


def main():
    """Utility script main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Google Maps Scraper Utilities")
    parser.add_argument("action", choices=["progress", "stats", "reset", "clean", "backup"],
                       help="Utility action to perform")
    
    args = parser.parse_args()
    
    if args.action == "progress":
        show_progress()
    elif args.action == "stats":
        show_data_stats()
    elif args.action == "reset":
        confirm = input("Are you sure you want to reset progress? (y/N): ")
        if confirm.lower() == 'y':
            reset_progress()
    elif args.action == "clean":
        clean_data()
    elif args.action == "backup":
        backup_data()


if __name__ == "__main__":
    main()
