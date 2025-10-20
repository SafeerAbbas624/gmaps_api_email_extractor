"""
Main runner script for Google Maps Scraper
Handles continuous operation, progress tracking, and error recovery
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime
from typing import List, Tuple
import argparse
from dotenv import load_dotenv

from scraper import GoogleMapsScraper
from data_manager import DataManager
from config import config


class ScraperRunner:
    """Main runner class that orchestrates the scraping process"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.running = True
        self.logger = logging.getLogger('gmaps_scraper.runner')

        # Initialize scraper with runner reference for shutdown handling
        self.scraper = GoogleMapsScraper(self)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def initialize(self):
        """Initialize the scraper system"""
        try:
            # Load environment variables from .env file
            from pathlib import Path
            env_path = Path('.') / '.env'
            load_dotenv(dotenv_path=env_path)

            # Also try loading from current directory explicitly
            import os
            if os.path.exists('.env'):
                load_dotenv('.env')

            # Validate configuration
            errors = config.validate()
            if errors:
                for error in errors:
                    self.logger.error(error)
                raise ValueError("Configuration validation failed")
            
            # Initialize data files
            self.data_manager.initialize_output_files()
            
            # Attempt crash recovery
            if config.enable_crash_recovery:
                recovered = self.data_manager.recover_from_crash()
                if recovered:
                    self.logger.info("Successfully recovered from previous crash")
            
            self.logger.info("Scraper system initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize scraper: {e}")
            raise
    
    def run_continuous_scraping(self):
        """Run continuous scraping operation"""
        try:
            # Load input data
            niches, locations = self.scraper.load_input_data()
            
            if not niches or not locations:
                self.logger.error("No niches or locations found to scrape")
                return
            
            self.logger.info(f"Starting continuous scraping for {len(niches)} niches and {len(locations)} locations")
            
            # Resume from saved progress
            niche_index = self.scraper.progress.get("current_niche_index", 0)
            location_index = self.scraper.progress.get("current_location_index", 0)
            
            total_combinations = len(niches) * len(locations)
            completed_combinations = niche_index * len(locations) + location_index
            
            self.logger.info(f"Resuming from niche {niche_index}, location {location_index}")
            self.logger.info(f"Progress: {completed_combinations}/{total_combinations} combinations completed")
            
            while self.running and niche_index < len(niches):
                niche = niches[niche_index]
                
                while self.running and location_index < len(locations):
                    city, state = locations[location_index]
                    location_str = f"{city}, {state}"
                    
                    try:
                        self.logger.info(f"Scraping: {niche} in {location_str}")
                        
                        # Scrape data for this niche/location combination
                        scraped_data = self.scraper.scrape_niche_location(niche, location_str)

                        if scraped_data:
                            self.logger.info(f"Found {len(scraped_data)} records")
                            # Save immediately to CSV for real-time email sending
                            self.data_manager.save_batch_data(scraped_data)
                        else:
                            self.logger.info(f"No results for {niche} in {location_str}")
                        
                        # Update progress
                        location_index += 1
                        self.scraper.progress["current_location_index"] = location_index
                        self.scraper._save_progress()
                        
                        # Add delay between location searches
                        time.sleep(config.delay_between_requests)
                        
                    except Exception as e:
                        self.logger.error(f"Error scraping {niche} in {location_str}: {e}")
                        location_index += 1  # Skip this location and continue
                        continue
                
                # Move to next niche
                niche_index += 1
                location_index = 0  # Reset location index for new niche
                
                # Update progress
                self.scraper.progress["current_niche_index"] = niche_index
                self.scraper.progress["current_location_index"] = location_index
                self.scraper._save_progress()
                
                self.logger.info(f"Completed niche: {niche}")

            if self.running:
                self.logger.info("Scraping completed for all niches and locations!")
            else:
                self.logger.info("Scraping stopped by user")
                
        except Exception as e:
            self.logger.error(f"Error in continuous scraping: {e}")
            raise
    
    def run_single_search(self, niche: str, location: str):
        """Run a single search for testing purposes"""
        try:
            self.logger.info(f"Running single search: {niche} in {location}")
            
            scraped_data = self.scraper.scrape_niche_location(niche, location)
            
            if scraped_data:
                self.data_manager.save_batch_data(scraped_data, backup=True)
                self.logger.info(f"Single search completed. Found {len(scraped_data)} results")
            else:
                self.logger.info("No results found for single search")
                
        except Exception as e:
            self.logger.error(f"Error in single search: {e}")
            raise
    
    def cleanup_and_finalize(self):
        """Clean up duplicates and create final output"""
        try:
            self.logger.info("Starting final cleanup and duplicate removal...")
            
            removed_count = self.data_manager.remove_duplicates_and_finalize()
            
            # Get final statistics
            stats = self.data_manager.get_data_stats()
            
            self.logger.info("=== SCRAPING SUMMARY ===")
            self.logger.info(f"Total records: {stats.get('total_records', 0)}")
            self.logger.info(f"Unique businesses: {stats.get('unique_businesses', 0)}")
            self.logger.info(f"Niches covered: {stats.get('niches_covered', 0)}")
            self.logger.info(f"Locations covered: {stats.get('locations_covered', 0)}")
            self.logger.info(f"Records with phone: {stats.get('records_with_phone', 0)}")
            self.logger.info(f"Records with website: {stats.get('records_with_website', 0)}")
            self.logger.info(f"Duplicates removed: {removed_count}")
            
        except Exception as e:
            self.logger.error(f"Error in cleanup: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Google Maps Business Scraper")
    parser.add_argument("--mode", choices=["continuous", "single", "cleanup"], 
                       default="continuous", help="Scraping mode")
    parser.add_argument("--niche", help="Niche for single search mode")
    parser.add_argument("--location", help="Location for single search mode")
    
    args = parser.parse_args()
    
    runner = ScraperRunner()
    
    try:
        # Initialize system
        runner.initialize()
        
        if args.mode == "continuous":
            runner.run_continuous_scraping()
            
        elif args.mode == "single":
            if not args.niche or not args.location:
                print("Error: --niche and --location are required for single mode")
                sys.exit(1)
            runner.run_single_search(args.niche, args.location)
            
        elif args.mode == "cleanup":
            runner.cleanup_and_finalize()
            
        # Always run cleanup at the end (unless it was the only operation)
        if args.mode != "cleanup":
            runner.cleanup_and_finalize()
            
    except KeyboardInterrupt:
        runner.logger.info("Scraping interrupted by user")
    except Exception as e:
        runner.logger.error(f"Fatal error: {e}")
        sys.exit(1)
    
    runner.logger.info("Scraper finished")


if __name__ == "__main__":
    main()
