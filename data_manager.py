"""
Data Management Module for Google Maps Scraper
Handles data persistence, crash recovery, and duplicate removal
"""

import pandas as pd
import os
import json
import logging
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import config


class DataManager:
    """Manages data persistence and recovery for the scraper"""
    
    def __init__(self):
        self.logger = logging.getLogger('gmaps_scraper.data_manager')
        self.backup_counter = 0
        
    def initialize_output_files(self):
        """Initialize output directories and files"""
        try:
            # Create directories
            os.makedirs(os.path.dirname(config.output_file), exist_ok=True)
            os.makedirs(os.path.dirname(config.progress_file), exist_ok=True)
            
            # Initialize CSV with headers if it doesn't exist
            if not os.path.exists(config.output_file):
                df = pd.DataFrame(columns=config.data_fields)
                df.to_csv(config.output_file, index=False)
                self.logger.info(f"Initialized output file: {config.output_file}")
            
            # Initialize temp file
            if not os.path.exists(config.temp_file):
                df = pd.DataFrame(columns=config.data_fields)
                df.to_csv(config.temp_file, index=False)
                self.logger.info(f"Initialized temp file: {config.temp_file}")
                
        except Exception as e:
            self.logger.error(f"Error initializing output files: {e}")
            raise
    
    def save_batch_data(self, data: List[Dict[str, str]], backup: bool = False):
        """Save a batch of scraped data - only saves records with valid emails"""
        if not data:
            return

        try:
            df = pd.DataFrame(data)

            # Filter out records with "NOT AVAILABLE" emails
            # Only save records that have valid email addresses
            df_filtered = df[df['email'] != 'NOT AVAILABLE'].copy()

            if len(df_filtered) == 0:
                self.logger.info(f"Skipped batch of {len(data)} records (no valid emails)")
                return

            # Append to both main and temp files
            for file_path in [config.output_file, config.temp_file]:
                df_filtered.to_csv(file_path, mode='a', header=False, index=False)

            self.logger.info(f"Saved batch of {len(df_filtered)} records (filtered from {len(data)})")

            # Create backup if requested
            if backup:
                self._create_backup()

            self.backup_counter += len(df_filtered)
            
            # Auto-backup every N records
            if self.backup_counter >= config.backup_interval:
                self._create_backup()
                self.backup_counter = 0
                
        except Exception as e:
            self.logger.error(f"Error saving batch data: {e}")
            raise
    
    def _create_backup(self):
        """Create a timestamped backup of the current data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = os.path.join(backup_dir, f"scraped_data_backup_{timestamp}.csv")
            
            if os.path.exists(config.output_file):
                shutil.copy2(config.output_file, backup_file)
                self.logger.info(f"Created backup: {backup_file}")
                
        except Exception as e:
            self.logger.warning(f"Error creating backup: {e}")
    
    def recover_from_crash(self) -> bool:
        """Attempt to recover data from a previous crash"""
        try:
            # Check if temp file has more recent data than main file
            if not os.path.exists(config.temp_file):
                return False
            
            temp_mtime = os.path.getmtime(config.temp_file)
            main_mtime = os.path.getmtime(config.output_file) if os.path.exists(config.output_file) else 0
            
            if temp_mtime > main_mtime:
                # Temp file is newer, merge data
                self.logger.info("Recovering data from temp file...")
                
                # Read both files
                temp_df = pd.read_csv(config.temp_file)
                main_df = pd.read_csv(config.output_file) if os.path.exists(config.output_file) else pd.DataFrame()
                
                # Combine and remove duplicates
                if not main_df.empty:
                    combined_df = pd.concat([main_df, temp_df], ignore_index=True)
                else:
                    combined_df = temp_df
                
                # Remove duplicates based on phone number
                clean_df = self._remove_duplicates_from_df(combined_df)
                
                # Save recovered data
                clean_df.to_csv(config.output_file, index=False)
                
                recovered_count = len(temp_df) - len(main_df) if not main_df.empty else len(temp_df)
                self.logger.info(f"Recovered {recovered_count} records from crash")
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error during crash recovery: {e}")
            
        return False
    
    def _remove_duplicates_from_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicates from DataFrame based on phone number"""
        try:
            # Remove duplicates based on phone number (excluding 'NOT AVAILABLE')
            df_with_phone = df[df['phone_number'] != 'NOT AVAILABLE'].drop_duplicates(subset=['phone_number'])
            
            # Keep records with 'NOT AVAILABLE' phone numbers (they might be unique)
            df_no_phone = df[df['phone_number'] == 'NOT AVAILABLE']
            
            # Combine back
            clean_df = pd.concat([df_with_phone, df_no_phone], ignore_index=True)
            
            return clean_df
            
        except Exception as e:
            self.logger.error(f"Error removing duplicates: {e}")
            return df
    
    def remove_duplicates_and_finalize(self, input_file: str = None, output_file: str = None) -> int:
        """Remove duplicates and create final clean CSV"""
        input_file = input_file or config.output_file
        
        if output_file is None:
            base_name = os.path.splitext(config.output_file)[0]
            output_file = f"{base_name}_final.csv"
        
        try:
            if not os.path.exists(input_file):
                self.logger.warning(f"Input file {input_file} does not exist")
                return 0
            
            # Read the data
            df = pd.read_csv(input_file)
            initial_count = len(df)
            
            if initial_count == 0:
                self.logger.info("No data to process")
                return 0
            
            # Remove duplicates
            clean_df = self._remove_duplicates_from_df(df)
            
            # Save final clean data
            clean_df.to_csv(output_file, index=False)
            
            removed_count = initial_count - len(clean_df)
            self.logger.info(f"Final cleanup: Removed {removed_count} duplicates from {initial_count} records")
            self.logger.info(f"Final clean file saved to: {output_file}")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"Error in final cleanup: {e}")
            return 0
    
    def get_data_stats(self) -> Dict[str, Any]:
        """Get statistics about the scraped data"""
        try:
            if not os.path.exists(config.output_file):
                return {"total_records": 0, "unique_businesses": 0, "niches_covered": 0}
            
            df = pd.read_csv(config.output_file)
            
            stats = {
                "total_records": len(df),
                "unique_businesses": len(df[df['phone_number'] != 'NOT AVAILABLE']['phone_number'].unique()),
                "niches_covered": len(df['niche'].unique()),
                "locations_covered": len(df['state'].unique()),
                "records_with_phone": len(df[df['phone_number'] != 'NOT AVAILABLE']),
                "records_with_website": len(df[df['website'] != 'NOT AVAILABLE'])
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting data stats: {e}")
            return {"error": str(e)}
