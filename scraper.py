"""
Google Maps Business Scraper
A robust scraper for extracting business information from Google Maps
"""

import googlemaps
import pandas as pd
import time
import logging
import json
import os
import csv
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import requests
from urllib.parse import quote
import random

from config import config
from email_scraper import EmailScraper


class GoogleMapsScraper:
    """Main scraper class for Google Maps business data"""
    
    def __init__(self, runner=None):
        self.gmaps = None
        self.session_requests = 0
        self.daily_requests = 0
        self.last_request_time = 0
        self.start_time = datetime.now()
        self.logger = self._setup_logging()
        self.runner = runner

        # Initialize email scraper with runner reference
        self.email_scraper = EmailScraper(runner)

        # Initialize Google Maps client
        self._initialize_gmaps_client()
        
        # Load or initialize progress tracking
        self.progress = self._load_progress()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
        
        logger = logging.getLogger('gmaps_scraper')
        logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(config.log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_gmaps_client(self):
        """Initialize Google Maps client with API key"""
        try:
            if not config.google_maps_api_key:
                raise ValueError("Google Maps API key not found")
            
            self.gmaps = googlemaps.Client(key=config.google_maps_api_key)
            self.logger.info("Google Maps client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Maps client: {e}")
            raise
    
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress from file or create new progress tracking"""
        if os.path.exists(config.progress_file):
            try:
                with open(config.progress_file, 'r') as f:
                    progress = json.load(f)
                self.logger.info(f"Loaded progress: {progress}")
                return progress
            except Exception as e:
                self.logger.warning(f"Could not load progress file: {e}")
        
        return {
            "current_niche_index": 0,
            "current_location_index": 0,
            "total_scraped": 0,
            "last_update": datetime.now().isoformat(),
            "daily_requests": 0,
            "last_request_date": datetime.now().date().isoformat()
        }
    
    def _save_progress(self):
        """Save current progress to file"""
        try:
            self.progress["last_update"] = datetime.now().isoformat()
            self.progress["total_scraped"] = getattr(self, 'total_scraped', 0)
            self.progress["daily_requests"] = self.daily_requests
            self.progress["last_request_date"] = datetime.now().date().isoformat()
            
            os.makedirs(os.path.dirname(config.progress_file), exist_ok=True)
            with open(config.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save progress: {e}")
    
    def _rate_limit(self):
        """Implement rate limiting to avoid API bans"""
        current_time = time.time()
        
        # Check daily limit
        today = datetime.now().date().isoformat()
        if self.progress.get("last_request_date") != today:
            self.daily_requests = 0
            self.progress["last_request_date"] = today
        
        if self.daily_requests >= config.max_daily_requests:
            self.logger.warning("Daily request limit reached. Waiting until tomorrow...")
            # Calculate time until midnight
            tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            sleep_time = (tomorrow - datetime.now()).total_seconds()
            time.sleep(sleep_time)
            self.daily_requests = 0
        
        # Rate limiting between requests
        time_since_last = current_time - self.last_request_time
        if time_since_last < config.delay_between_requests:
            sleep_time = config.delay_between_requests - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.session_requests += 1
        self.daily_requests += 1
    
    def _search_places(self, query: str, location: str) -> List[Dict[str, Any]]:
        """Search for places using Google Maps Places API with maximum results"""
        all_places = []
        seen_place_ids = set()

        # Multiple search strategies to get maximum results
        search_variations = [
            f"{query} in {location}",
            f"{query} near {location}",
            f"{query} {location}",
        ]

        for search_query in search_variations:
            if len(all_places) >= config.max_results_per_search:
                break

            self._rate_limit()

            try:
                self.logger.info(f"Searching for: {search_query}")

                # Use text search
                results = self.gmaps.places(
                    query=search_query,
                    type='establishment'
                )

                places = results.get('results', [])

                # Get additional results using pagination
                next_page_token = results.get('next_page_token')
                page_count = 0
                max_pages = 3  # Google typically allows up to 3 pages (60 results max per search)

                while next_page_token and page_count < max_pages and len(all_places) < config.max_results_per_search:
                    time.sleep(3)  # Required delay for next_page_token (increased to 3 seconds)
                    self._rate_limit()

                    try:
                        next_results = self.gmaps.places(
                            page_token=next_page_token
                        )
                        new_places = next_results.get('results', [])
                        places.extend(new_places)
                        next_page_token = next_results.get('next_page_token')
                        page_count += 1

                        self.logger.info(f"Got page {page_count + 1}, total places so far: {len(places)}")

                    except Exception as e:
                        self.logger.warning(f"Error getting next page: {e}")
                        break

                # Add unique places only
                for place in places:
                    place_id = place.get('place_id', '')
                    if place_id and place_id not in seen_place_ids:
                        seen_place_ids.add(place_id)
                        all_places.append(place)

                        if len(all_places) >= config.max_results_per_search:
                            break

                self.logger.info(f"Found {len(places)} places for query: {search_query} (unique: {len(all_places)} total)")

            except Exception as e:
                self.logger.error(f"Error in search variation '{search_query}': {e}")
                continue

        final_count = len(all_places)
        self.logger.info(f"Final result: {final_count} unique places found")

        return all_places
    
    def _get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Get detailed information for a specific place"""
        self._rate_limit()
        
        try:
            fields = [
                'name', 'formatted_address', 'formatted_phone_number',
                'website', 'url', 'place_id', 'geometry'
            ]
            
            details = self.gmaps.place(
                place_id=place_id,
                fields=fields
            )
            
            return details.get('result', {})
            
        except Exception as e:
            self.logger.error(f"Error getting place details for {place_id}: {e}")
            return {}
    
    def _extract_business_data(self, place: Dict[str, Any], niche: str, location: str) -> Dict[str, str]:
        """Extract and format business data from place information"""
        
        # Get detailed information
        place_id = place.get('place_id', '')
        details = {}
        
        if place_id:
            details = self._get_place_details(place_id)
        
        # Combine basic and detailed info
        combined_data = {**place, **details}
        
        # Extract state from address
        address = combined_data.get('formatted_address', 'NOT AVAILABLE')
        state = self._extract_state_from_address(address)
        
        # Create Google Maps URL
        maps_url = combined_data.get('url', 'NOT AVAILABLE')
        if maps_url == 'NOT AVAILABLE' and place_id:
            maps_url = f"https://maps.google.com/maps/place/?q=place_id:{place_id}"

        # Extract email using both methods
        business_name = combined_data.get('name', '')
        website_url = combined_data.get('website', 'NOT AVAILABLE')
        email = self.email_scraper.get_business_email(combined_data, website_url, business_name)

        return {
            'name': combined_data.get('name', 'NOT AVAILABLE'),
            'niche': niche,
            'address': address,
            'state': state,
            'phone_number': combined_data.get('formatted_phone_number', 'NOT AVAILABLE'),
            'website': website_url,
            'email': email,
            'result_url': maps_url
        }
    
    def _extract_state_from_address(self, address: str) -> str:
        """Extract state/region from formatted address (supports US states and Italian regions)"""
        if address == 'NOT AVAILABLE':
            return 'NOT AVAILABLE'

        try:
            # US state abbreviations
            us_states = {
                'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
            }

            # Italian regions and provinces
            italian_regions = {
                'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
                'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche',
                'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana',
                'Trentino-Alto Adige', 'Umbria', 'Valle d\'Aosta', 'Veneto'
            }

            # Italian province abbreviations
            italian_provinces = {
                'AG', 'AL', 'AN', 'AO', 'AR', 'AP', 'AT', 'AV', 'BA', 'BT', 'BL',
                'BN', 'BG', 'BI', 'BO', 'BZ', 'BS', 'BR', 'CA', 'CL', 'CB', 'CI',
                'CE', 'CT', 'CZ', 'CH', 'CO', 'CS', 'CR', 'KR', 'CN', 'EN', 'FM',
                'FE', 'FI', 'FG', 'FC', 'FR', 'GE', 'GO', 'GR', 'IM', 'IS', 'SP',
                'AQ', 'LT', 'LE', 'LC', 'LI', 'LO', 'LU', 'MC', 'MN', 'MS', 'MT',
                'VS', 'ME', 'MI', 'MO', 'MB', 'NA', 'NO', 'NU', 'OG', 'OT', 'OR',
                'PD', 'PA', 'PR', 'PV', 'PG', 'PU', 'PE', 'PC', 'PI', 'PT', 'PN',
                'PZ', 'PO', 'RG', 'RA', 'RC', 'RE', 'RI', 'RN', 'RM', 'RO', 'SA',
                'SS', 'SV', 'SI', 'SO', 'SR', 'TA', 'TE', 'TR', 'TO', 'TP', 'TN',
                'TV', 'TS', 'UD', 'VA', 'VE', 'VB', 'VC', 'VR', 'VV', 'VI', 'VT'
            }
            
            # Split address and look for state/region
            parts = address.split(', ')

            # Check for Italian regions (full names)
            for part in parts:
                part_clean = part.strip()
                if part_clean in italian_regions:
                    return part_clean

            # Check for province abbreviations and US states
            for part in parts:
                words = part.strip().split()
                for word in words:
                    word_upper = word.upper()
                    if word_upper in us_states or word_upper in italian_provinces:
                        return word_upper

            # Check if "Italy" or "Italia" is in address
            address_lower = address.lower()
            if 'italy' in address_lower or 'italia' in address_lower:
                return 'Italy'

            return 'NOT AVAILABLE'
            
        except Exception:
            return 'NOT AVAILABLE'

    def _save_data_to_csv(self, data: List[Dict[str, str]], append: bool = True):
        """Save scraped data to CSV file"""
        try:
            os.makedirs(os.path.dirname(config.output_file), exist_ok=True)

            df = pd.DataFrame(data)

            # Save to temporary file first (for crash recovery)
            df.to_csv(config.temp_file, mode='a' if append else 'w',
                     header=not (append and os.path.exists(config.temp_file)),
                     index=False)

            # Also save to main file
            df.to_csv(config.output_file, mode='a' if append else 'w',
                     header=not (append and os.path.exists(config.output_file)),
                     index=False)

            self.logger.info(f"Saved {len(data)} records to CSV")

        except Exception as e:
            self.logger.error(f"Error saving data to CSV: {e}")
            raise

    def scrape_niche_location(self, niche: str, location: str, data_manager=None) -> List[Dict[str, str]]:
        """Scrape businesses for a specific niche and location"""
        query = f"{niche} in {location}"

        try:
            # Search for places
            places = self._search_places(niche, location)

            if not places:
                self.logger.info(f"No results found for {query}")
                return []

            scraped_data = []
            saved_count = 0

            for place in places:
                # Check if we should stop (Ctrl+C was pressed)
                if self.runner and not self.runner.running:
                    self.logger.info("Shutdown requested, stopping business processing")
                    break

                try:
                    business_data = self._extract_business_data(place, niche, location)
                    scraped_data.append(business_data)

                    # Save immediately if has valid email and data_manager is available
                    if data_manager and business_data.get('email') != 'NOT AVAILABLE':
                        data_manager.save_batch_data([business_data])
                        saved_count += 1

                    # Add small delay between processing each business
                    time.sleep(random.uniform(0.5, 1.5))

                except Exception as e:
                    self.logger.warning(f"Error processing place {place.get('name', 'Unknown')}: {e}")
                    continue

            self.logger.info(f"Successfully scraped {len(scraped_data)} businesses for {query} ({saved_count} saved with emails)")
            return scraped_data

        except Exception as e:
            self.logger.error(f"Error scraping {query}: {e}")
            return []

    def load_input_data(self) -> Tuple[List[str], List[Tuple[str, str]]]:
        """Load niches and locations from CSV files"""
        try:
            # Load niches
            niches_df = pd.read_csv(config.niches_file)
            niches = niches_df['niche'].tolist()

            # Load locations
            locations_df = pd.read_csv(config.locations_file)
            locations = list(zip(locations_df['city'], locations_df['state']))

            self.logger.info(f"Loaded {len(niches)} niches and {len(locations)} locations")
            return niches, locations

        except Exception as e:
            self.logger.error(f"Error loading input data: {e}")
            raise

    def remove_duplicates(self, input_file: str = None, output_file: str = None) -> int:
        """Remove duplicates based on phone number and save clean data"""
        input_file = input_file or config.output_file
        output_file = output_file or config.output_file.replace('.csv', '_clean.csv')

        try:
            if not os.path.exists(input_file):
                self.logger.warning(f"Input file {input_file} does not exist")
                return 0

            # Read the data
            df = pd.read_csv(input_file)
            initial_count = len(df)

            # Remove duplicates based on phone number (excluding 'NOT AVAILABLE')
            df_clean = df[df['phone_number'] != 'NOT AVAILABLE'].drop_duplicates(subset=['phone_number'])

            # Add back records with 'NOT AVAILABLE' phone numbers (they might be unique businesses)
            df_no_phone = df[df['phone_number'] == 'NOT AVAILABLE']
            df_clean = pd.concat([df_clean, df_no_phone], ignore_index=True)

            # Save clean data
            df_clean.to_csv(output_file, index=False)

            removed_count = initial_count - len(df_clean)
            self.logger.info(f"Removed {removed_count} duplicates. Clean file saved to {output_file}")

            return removed_count

        except Exception as e:
            self.logger.error(f"Error removing duplicates: {e}")
            return 0
