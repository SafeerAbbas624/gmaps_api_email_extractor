"""
FREE Google Maps Scraper using SeleniumBase UC Mode
No API costs - 100% FREE scraping with anti-detection
"""

import time
import random
import logging
import json
import os
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from email_scraper import EmailScraper
from rate_limiter import RateLimiter
from simple_email_manager import SimpleEmailManager


class SeleniumBaseScraper:
    """FREE Google Maps scraper using SeleniumBase UC Mode"""

    def __init__(self, runner=None):
        self.logger = self._setup_logging()
        self.runner = runner
        self.email_scraper = EmailScraper(runner)
        self.rate_limiter = RateLimiter()
        self.email_manager = SimpleEmailManager()
        self.progress = self._load_progress()
        self.total_scraped = 0
        self._sb_context = None  # Store SeleniumBase context manager for cleanup

        # Daily stats tracking
        self.daily_stats = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'searches_today': 0,
            'businesses_today': 0,
            'emails_today': 0,
            'start_time': datetime.now()
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        os.makedirs("logs", exist_ok=True)
        
        logger = logging.getLogger('seleniumbase_scraper')
        logger.setLevel(logging.INFO)
        
        # File handler with UTF-8 encoding
        file_handler = logging.FileHandler('logs/scraper.log', encoding='utf-8')
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
    
    def _create_scraper_completion_flag(self):
        """Create a flag file to signal that scraping is complete"""
        try:
            flag_file = "scraper_complete.flag"
            with open(flag_file, 'w') as f:
                f.write(f"Scraper completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total businesses scraped: {self.total_scraped}\n")
            self.logger.info(f"Scraper completion flag created: {flag_file}")
        except Exception as e:
            self.logger.error(f"Error creating completion flag: {e}")

    def _load_progress(self) -> Dict[str, Any]:
        """Load progress from file"""
        progress_file = "output/progress.json"
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
                self.logger.info(f"Loaded progress: {progress}")
                return progress
            except Exception as e:
                self.logger.warning(f"Could not load progress: {e}")
        
        return {
            "current_niche_index": 0,
            "current_location_index": 0,
            "total_scraped": 0,
            "last_update": datetime.now().isoformat()
        }
    
    def _save_progress(self):
        """Save progress to file"""
        try:
            self.progress["last_update"] = datetime.now().isoformat()
            self.progress["total_scraped"] = self.total_scraped

            os.makedirs("output", exist_ok=True)
            with open("output/progress.json", 'w') as f:
                json.dump(self.progress, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving progress: {e}")

    def _check_and_log_daily_summary(self, niches, locations):
        """Check if day changed and log daily summary"""
        current_date = datetime.now().strftime('%Y-%m-%d')

        if current_date != self.daily_stats['date']:
            # Log previous day summary
            self._log_daily_summary(niches, locations)

            # Reset for new day
            self.daily_stats = {
                'date': current_date,
                'searches_today': 0,
                'businesses_today': 0,
                'emails_today': 0,
                'start_time': datetime.now()
            }

    def _log_daily_summary(self, niches, locations):
        """Log daily summary"""
        runtime = datetime.now() - self.daily_stats['start_time']
        hours = int(runtime.total_seconds() // 3600)
        minutes = int((runtime.total_seconds() % 3600) // 60)

        # Get total stats from email manager
        email_stats = self.email_manager.get_stats()

        # Get progress info
        total_combinations = len(niches) * len(locations)
        current_combination = (self.progress.get('current_niche_index', 0) * len(locations) +
                              self.progress.get('current_location_index', 0))
        remaining_combinations = total_combinations - current_combination

        self.logger.info("=" * 100)
        self.logger.info(f"DAILY SUMMARY - {self.daily_stats['date']}")
        self.logger.info("=" * 100)
        self.logger.info(f"Runtime: {hours}h {minutes}m")
        self.logger.info(f"Searches today: {self.daily_stats['searches_today']}")
        self.logger.info(f"Businesses scraped today: {self.daily_stats['businesses_today']}")
        self.logger.info(f"Emails found today: {self.daily_stats['emails_today']}")
        self.logger.info("-" * 100)
        self.logger.info(f"Total combinations: {total_combinations}")
        self.logger.info(f"Completed: {current_combination} ({current_combination/total_combinations*100:.1f}%)")
        self.logger.info(f"Remaining: {remaining_combinations}")
        self.logger.info("-" * 100)
        self.logger.info(f"Total emails collected: {email_stats['total_collected']}")
        self.logger.info(f"Total emails sent: {email_stats['total_sent']}")
        self.logger.info(f"Total emails unsent: {email_stats['unsent']}")
        self.logger.info("=" * 100)

    def load_input_files(self) -> tuple:
        """Load niches and locations from CSV files"""
        try:
            # Load niches
            with open('input/niches.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                niches = [row['niche'] for row in reader]
            
            # Load locations
            with open('input/locations.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                locations = [(row['city'], row['state']) for row in reader]
            
            self.logger.info(f"Loaded {len(niches)} niches and {len(locations)} locations")
            return niches, locations

        except Exception as e:
            self.logger.error(f"Error loading input files: {e}")
            raise
    
    def search_google_maps(self, sb, niche: str, city: str, state: str) -> List[Dict]:
        """Search Google Maps and extract business data"""
        search_query = f"{niche} in {city}, {state}"
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"

        self.logger.info(f"Searching: {search_query}")

        # Track daily stats
        self.daily_stats['searches_today'] += 1

        try:
            # Open URL with UC Mode (undetected)
            sb.uc_open_with_reconnect(url, reconnect_time=4)

            # Wait for results to load
            time.sleep(random.uniform(3, 5))

            # Scroll to load more results
            self._scroll_results(sb)

            # Extract business data
            businesses = self._extract_businesses(sb, niche)

            # Track businesses found
            self.daily_stats['businesses_today'] += len(businesses)

            self.logger.info(f"Found {len(businesses)} businesses")
            return businesses

        except Exception as e:
            self.logger.error(f"Error searching Google Maps: {e}")
            return []
    
    def _scroll_results(self, sb):
        """Scroll the results panel to load more businesses"""
        try:
            # Find the scrollable results panel
            scrollable_div = sb.driver.find_element(
                By.CSS_SELECTOR, 
                'div[role="feed"]'
            )
            
            # Scroll multiple times to load more results
            for i in range(5):  # Scroll 5 times
                sb.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", 
                    scrollable_div
                )
                time.sleep(random.uniform(1, 2))  # Human-like delay
                
        except Exception as e:
            self.logger.warning(f"Could not scroll results: {e}")
    
    def _extract_businesses(self, sb, niche: str) -> List[Dict]:
        """Extract business information from search results"""
        businesses = []
        
        try:
            # Wait for business cards to load
            time.sleep(2)
            
            # Find all business result cards
            # Use the correct selector that works
            business_cards = sb.driver.find_elements(
                By.CSS_SELECTOR,
                'div[role="feed"] > div'
            )
            
            self.logger.info(f"Found {len(business_cards)} business cards")
            
            for card in business_cards[:20]:  # Limit to 20 per search
                try:
                    business_data = self._extract_business_data(sb, card, niche)
                    if business_data:
                        businesses.append(business_data)
                except Exception as e:
                    self.logger.warning(f"Error extracting business: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Error finding business cards: {e}")
        
        return businesses
    
    def _extract_business_data(self, sb, card, niche: str) -> Optional[Dict]:
        """Extract data from a single business card"""
        try:
            # Click on the business card to open details
            card.click()
            time.sleep(random.uniform(2, 3))
            
            # Extract business name
            name = self._safe_extract(sb, 'h1.DUwDvf')
            
            # Extract address
            address = self._safe_extract(sb, 'button[data-item-id="address"]')
            
            # Extract phone
            phone = self._safe_extract(sb, 'button[data-item-id^="phone"]')
            
            # Extract website
            website = self._safe_extract_attribute(
                sb, 
                'a[data-item-id="authority"]', 
                'href'
            )
            
            # Extract Google Maps URL
            result_url = sb.driver.current_url
            
            # Extract state from address
            state = self._extract_state(address)

            # Try to extract email from Google Maps first (faster)
            email = self._extract_email_from_gmaps(sb)
            email_source = ""

            # If no email on Google Maps, scrape from website
            if not email and website:
                self.logger.info(f"No email on Google Maps, scraping website: {website}")
                email = self.email_scraper.scrape_email_from_website(website)
                if email:
                    email_source = "website"
            elif email:
                self.logger.info(f"Email found on Google Maps: {email}")
                email_source = "gmaps"
            
            business_data = {
                'name': name,
                'niche': niche,
                'address': address,
                'state': state,
                'phone_number': phone,
                'website': website,
                'email': email,
                'email_source': email_source,
                'result_url': result_url
            }
            
            self.logger.info(f"Extracted: {name}")
            return business_data
            
        except Exception as e:
            self.logger.warning(f"Error extracting business data: {e}")
            return None
    
    def _extract_email_from_gmaps(self, sb) -> str:
        """Try to extract email directly from Google Maps page"""
        try:
            import re

            # Try to find email in mailto links
            try:
                email_link = sb.driver.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]')
                href = email_link.get_attribute('href')
                if href:
                    email = href.replace('mailto:', '').strip()
                    return email
            except:
                pass

            # Try to find email in buttons with email data-item-id
            try:
                email_button = sb.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="email"]')
                text = email_button.text.strip()
                # Extract email using regex
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, text)
                if emails:
                    return emails[0]
            except:
                pass

            # Try to find email in the main content area text
            try:
                content_area = sb.driver.find_element(By.CSS_SELECTOR, 'div[role="main"]')
                all_text = content_area.text
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, all_text)
                if emails:
                    # Filter out common false positives
                    for email in emails:
                        if not any(x in email.lower() for x in ['example.com', 'test.com', 'google.com']):
                            return email
            except:
                pass

            return ""

        except Exception as e:
            return ""

    def _safe_extract(self, sb, selector: str) -> str:
        """Safely extract text from element"""
        try:
            element = sb.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except:
            return ""
    
    def _safe_extract_attribute(self, sb, selector: str, attribute: str) -> str:
        """Safely extract attribute from element"""
        try:
            element = sb.driver.find_element(By.CSS_SELECTOR, selector)
            return element.get_attribute(attribute)
        except:
            return ""
    
    def _extract_state(self, address: str) -> str:
        """Extract state/province from address"""
        if not address:
            return ""
        
        # Italian provinces (2-letter codes)
        provinces = ['RM', 'MI', 'NA', 'TO', 'PA', 'GE', 'BO', 'FI', 'BA', 'CT']
        
        for province in provinces:
            if province in address:
                return province
        
        return ""
    
    def save_to_csv(self, businesses: List[Dict], filename: str = "output/scraped_data.csv"):
        """Save businesses to CSV file"""
        try:
            os.makedirs("output", exist_ok=True)
            
            # Check if file exists
            file_exists = os.path.exists(filename)
            
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                fieldnames = ['name', 'niche', 'address', 'state', 'phone_number', 
                             'website', 'email', 'result_url']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Write header if new file
                if not file_exists:
                    writer.writeheader()
                
                # Write businesses
                for business in businesses:
                    # Remove email_source field (only used for testing)
                    business_copy = {k: v for k, v in business.items() if k in fieldnames}
                    writer.writerow(business_copy)

                    # Add email to email manager if valid
                    email = business.get('email', '')
                    name = business.get('name', '')
                    if self.email_manager.add_email(email, name):
                        self.logger.info(f"New email added: {email}")
                        self.daily_stats['emails_today'] += 1

            self.logger.info(f"Saved {len(businesses)} businesses to {filename}")

        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")

    def _is_session_valid(self, sb) -> bool:
        """Check if the browser session is still valid"""
        try:
            # Try to get current URL - this will fail if session is dead
            _ = sb.driver.current_url
            return True
        except Exception as e:
            self.logger.warning(f"Session check failed: {e}")
            return False

    def _create_new_session(self):
        """Create a new SeleniumBase session"""
        self.logger.info("🔄 Creating new browser session...")
        # SB() returns a context manager, __enter__() returns the actual sb object
        sb_context = SB(uc=True, headless=False, incognito=True)
        sb = sb_context.__enter__()
        # Store context manager for later cleanup
        self._sb_context = sb_context
        self.logger.info("✅ New browser session created successfully")
        return sb

    def _close_session(self, sb):
        """Safely close a browser session"""
        try:
            if hasattr(self, '_sb_context') and self._sb_context:
                self._sb_context.__exit__(None, None, None)
                self._sb_context = None
                self.logger.info("🔒 Browser session closed")
        except Exception as e:
            self.logger.warning(f"Error closing session: {e}")

    def _wait_with_keepalive(self, sb, wait_seconds: float):
        """Wait while keeping browser session alive with periodic activity"""
        KEEPALIVE_INTERVAL = 30  # Keep browser alive every 30 seconds

        remaining = wait_seconds
        while remaining > 0:
            sleep_time = min(KEEPALIVE_INTERVAL, remaining)
            time.sleep(sleep_time)
            remaining -= sleep_time

            # Keep session alive by doing a simple action
            if remaining > 0:
                try:
                    # Simple JavaScript execution to keep session alive
                    sb.driver.execute_script("return true;")
                except Exception as e:
                    self.logger.warning(f"Keepalive failed (session may have died): {e}")
                    return False  # Session died
        return True  # Session still alive

    def run(self):
        """Main scraping loop with automatic session recovery"""
        self.logger.info("Starting FREE Google Maps Scraper (SeleniumBase UC Mode)")
        self.logger.info("=" * 80)

        # Load input files
        niches, locations = self.load_input_files()

        total_combinations = len(niches) * len(locations)
        self.logger.info(f"Total search combinations: {total_combinations}")
        self.logger.info(f"Niches: {len(niches)}, Locations: {len(locations)}")
        self.logger.info("=" * 80)

        # Get starting indices from progress
        start_niche_idx = self.progress.get('current_niche_index', 0)
        start_location_idx = self.progress.get('current_location_index', 0)

        self.logger.info(f"Starting from: Niche {start_niche_idx}, Location {start_location_idx}")

        # Initialize browser session
        sb = self._create_new_session()
        consecutive_errors = 0
        MAX_CONSECUTIVE_ERRORS = 5

        try:
            # Loop through niches and locations
            for niche_idx in range(start_niche_idx, len(niches)):
                niche = niches[niche_idx]

                # Start from saved location index for first niche, 0 for others
                loc_start = start_location_idx if niche_idx == start_niche_idx else 0

                for loc_idx in range(loc_start, len(locations)):
                    city, state = locations[loc_idx]

                    try:
                        # Check if day changed and log summary
                        self._check_and_log_daily_summary(niches, locations)

                        # Check rate limits and wait if needed (with keepalive)
                        wait_time = self.rate_limiter.get_wait_time()
                        if wait_time > 0:
                            self.logger.info(f"⏳ Rate limit wait: {wait_time:.1f}s")
                            session_alive = self._wait_with_keepalive(sb, wait_time)
                            if not session_alive:
                                self.logger.warning("🔄 Session died during wait, restarting...")
                                self._close_session(sb)
                                sb = self._create_new_session()
                            self.rate_limiter.record_request()
                        else:
                            self.rate_limiter.wait_if_needed()

                        # Check session health before each search
                        if not self._is_session_valid(sb):
                            self.logger.warning("🔄 Invalid session detected, restarting browser...")
                            self._close_session(sb)
                            sb = self._create_new_session()
                            consecutive_errors = 0

                        # Search Google Maps
                        businesses = self.search_google_maps(sb, niche, city, state)

                        # Check if search succeeded (reset error counter)
                        if businesses is not None:
                            consecutive_errors = 0
                        else:
                            consecutive_errors += 1

                        # If too many consecutive errors, restart session
                        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                            self.logger.warning(f"🔄 {MAX_CONSECUTIVE_ERRORS} consecutive errors, restarting browser...")
                            self._close_session(sb)
                            sb = self._create_new_session()
                            consecutive_errors = 0

                        # Save results
                        if businesses:
                            self.save_to_csv(businesses)
                            self.total_scraped += len(businesses)

                        # Update progress
                        self.progress['current_niche_index'] = niche_idx
                        self.progress['current_location_index'] = loc_idx
                        self._save_progress()

                        # Log progress
                        completed = (niche_idx * len(locations)) + loc_idx + 1
                        progress_pct = (completed / total_combinations) * 100
                        self.logger.info(
                            f"Progress: {completed}/{total_combinations} "
                            f"({progress_pct:.1f}%) | Total scraped: {self.total_scraped}"
                        )

                    except KeyboardInterrupt:
                        self.logger.warning("Interrupted by user. Saving progress...")
                        self._save_progress()
                        raise

                    except Exception as e:
                        self.logger.error(f"Error processing {niche} in {city}: {e}")
                        consecutive_errors += 1

                        # Check if it's a session error
                        if "invalid session" in str(e).lower() or "session" in str(e).lower():
                            self.logger.warning("🔄 Session error detected, restarting browser...")
                            self._close_session(sb)
                            sb = self._create_new_session()
                            consecutive_errors = 0
                        continue

        finally:
            # Always close the session
            self._close_session(sb)

        # Log final daily summary
        self._log_daily_summary(niches, locations)

        self.logger.info("=" * 80)
        self.logger.info(f"SCRAPING COMPLETE! Total businesses scraped: {self.total_scraped}")
        self.logger.info("=" * 80)

        # Create completion flag file to signal sender that scraping is done
        self._create_scraper_completion_flag()


# Main entry point
if __name__ == "__main__":
    scraper = SeleniumBaseScraper()
    scraper.run()

