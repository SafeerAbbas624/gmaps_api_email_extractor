"""
Email Scraper Module for Google Maps Scraper
Extracts email addresses from business websites with Italian/English support
"""

import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
import time
from typing import List, Optional, Set
from config import config


class EmailScraper:
    """Scrapes email addresses from business websites"""
    
    def __init__(self, runner=None):
        self.logger = logging.getLogger('gmaps_scraper.email_scraper')
        self.session = requests.Session()
        self.runner = runner  # Reference to runner to check if we should stop
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Email regex pattern - more strict to avoid capturing extra text
        # Matches: word@domain.extension with proper boundaries
        self.email_pattern = re.compile(
            r'(?:^|[\s,;:\(\)\[\]<>"\'])'  # Start or whitespace/punctuation
            r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'  # Email
            r'(?:[\s,;:\(\)\[\]<>"\']|$)',  # End or whitespace/punctuation
            re.MULTILINE
        )
        
        # Contact page keywords in Italian and English
        self.contact_keywords = {
            'italian': [
                'contatti', 'contatto', 'contattaci', 'chi-siamo', 'chi_siamo',
                'informazioni', 'info', 'dove-siamo', 'dove_siamo', 'recapiti'
            ],
            'english': [
                'contact', 'contacts', 'contact-us', 'contact_us', 'about',
                'about-us', 'about_us', 'info', 'information', 'reach-us'
            ]
        }
        
        # Common email prefixes to prioritize
        self.priority_prefixes = [
            'info', 'contact', 'hello', 'mail', 'office', 'admin',
            'support', 'sales', 'business', 'general'
        ]
        
        # Emails to ignore (common false positives)
        self.ignore_emails = {
            'example@example.com', 'test@test.com', 'email@example.com',
            'info@example.com', 'contact@example.com', 'admin@example.com',
            'support@google.com', 'noreply@google.com', 'privacy@google.com'
        }
    
    def extract_email_from_google_data(self, place_data: dict) -> Optional[str]:
        """Extract email from Google Maps place data if available"""
        try:
            # Check various fields where email might be present
            fields_to_check = [
                'formatted_address', 'vicinity', 'name', 
                'editorial_summary', 'reviews'
            ]
            
            for field in fields_to_check:
                if field in place_data and place_data[field]:
                    text = str(place_data[field])
                    emails = self.email_pattern.findall(text)
                    
                    if emails:
                        # Return the first valid email found
                        for email in emails:
                            if email.lower() not in self.ignore_emails:
                                self.logger.info(f"Found email in Google data: {email}")
                                return email.lower()
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error extracting email from Google data: {e}")
            return None
    
    def scrape_email_from_website(self, website_url: str, business_name: str = "") -> Optional[str]:
        """Scrape email from business website"""
        if not website_url or website_url == 'NOT AVAILABLE':
            return None
        
        try:
            # Clean and validate URL
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            self.logger.info(f"Scraping email from website: {website_url}")
            
            # Get domain for email validation
            domain = urlparse(website_url).netloc.lower()
            
            # Try multiple pages
            pages_to_try = self._get_pages_to_scrape(website_url)
            
            for page_url in pages_to_try:
                # Check if we should stop (Ctrl+C was pressed)
                if self.runner and not self.runner.running:
                    return None

                email = self._scrape_page_for_email(page_url, domain, business_name)
                if email:
                    return email

                # Small delay between page requests
                time.sleep(1)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error scraping email from {website_url}: {e}")
            return None
    
    def _get_pages_to_scrape(self, base_url: str) -> List[str]:
        """Get list of pages to scrape for emails"""
        pages = [base_url]  # Start with homepage
        
        try:
            # Parse base URL
            parsed = urlparse(base_url)
            base_domain = f"{parsed.scheme}://{parsed.netloc}"
            
            # Add contact pages in both languages
            all_keywords = (self.contact_keywords['italian'] + 
                          self.contact_keywords['english'])
            
            for keyword in all_keywords[:config.max_pages_per_website - 1]:
                # Try different URL patterns
                contact_urls = [
                    f"{base_domain}/{keyword}",
                    f"{base_domain}/{keyword}.html",
                    f"{base_domain}/{keyword}.php",
                    f"{base_url.rstrip('/')}/{keyword}",
                ]
                
                pages.extend(contact_urls)
            
            # Limit total pages
            return pages[:config.max_pages_per_website * 4]
            
        except Exception as e:
            self.logger.warning(f"Error generating pages list: {e}")
            return [base_url]
    
    def _scrape_page_for_email(self, url: str, domain: str, business_name: str = "") -> Optional[str]:
        """Scrape a single page for email addresses"""
        try:
            response = self.session.get(
                url, 
                timeout=config.website_timeout,
                allow_redirects=True
            )
            
            if response.status_code != 200:
                return None
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content with better word boundary preservation
            text = soup.get_text(separator=' ', strip=True)

            # Add newlines between common separators to preserve boundaries
            text = re.sub(r'([,;:\(\)\[\]<>"\'])', r'\1\n', text)

            # Find all emails using the improved regex
            matches = self.email_pattern.finditer(text)
            emails = [match.group(1) for match in matches]
            
            if not emails:
                return None
            
            # Filter and prioritize emails
            valid_emails = []

            for email in emails:
                email = email.lower().strip()

                # Skip ignored emails
                if email in self.ignore_emails:
                    continue

                # Validate email format strictly
                if not self._is_valid_email(email):
                    continue

                # Prefer emails from the same domain
                email_domain = email.split('@')[1] if '@' in email else ''

                # Check if email domain matches or is related to website domain
                if (email_domain in domain or
                    domain.replace('www.', '') in email_domain or
                    any(part in email_domain for part in domain.split('.') if len(part) > 3)):
                    valid_emails.append(email)
            
            if valid_emails:
                # Prioritize by prefix
                for prefix in self.priority_prefixes:
                    for email in valid_emails:
                        if email.startswith(prefix + '@'):
                            self.logger.info(f"Found priority email: {email}")
                            return email
                
                # Return first valid email
                self.logger.info(f"Found email: {valid_emails[0]}")
                return valid_emails[0]
            
            return None
            
        except requests.exceptions.Timeout:
            self.logger.warning(f"Timeout scraping {url}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Request error scraping {url}: {e}")
            return None
        except Exception as e:
            self.logger.warning(f"Error scraping {url}: {e}")
            return None
    
    def get_business_email(self, place_data: dict, website_url: str, business_name: str = "") -> str:
        """
        Get business email using both methods:
        1. Check Google Maps data first
        2. Scrape website if no email found
        """
        try:
            # Check if we should stop (Ctrl+C was pressed)
            if self.runner and not self.runner.running:
                return "NOT AVAILABLE"

            # Method 1: Check Google Maps data
            email = self.extract_email_from_google_data(place_data)
            if email:
                return email

            # Check again before website scraping
            if self.runner and not self.runner.running:
                return "NOT AVAILABLE"

            # Method 2: Scrape website
            if config.enable_email_scraping:
                email = self.scrape_email_from_website(website_url, business_name)
                if email:
                    return email

            return "NOT AVAILABLE"

        except Exception as e:
            self.logger.error(f"Error getting business email: {e}")
            return "NOT AVAILABLE"

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format strictly to avoid false positives
        """
        if not email or '@' not in email:
            return False

        try:
            local, domain = email.rsplit('@', 1)

            # Local part validation
            if not local or len(local) > 64:
                return False

            # Check for invalid characters in local part
            if not re.match(r'^[A-Za-z0-9._%+-]+$', local):
                return False

            # Domain validation
            if not domain or len(domain) < 4:  # min: a.co
                return False

            # Domain must have at least one dot
            if '.' not in domain:
                return False

            # Check for invalid characters in domain
            if not re.match(r'^[A-Za-z0-9.-]+$', domain):
                return False

            # Domain parts validation
            parts = domain.split('.')
            for part in parts:
                if not part or len(part) > 63:
                    return False
                if not re.match(r'^[A-Za-z0-9-]+$', part):
                    return False
                if part.startswith('-') or part.endswith('-'):
                    return False

            # TLD must be at least 2 characters and only letters
            tld = parts[-1]
            if len(tld) < 2 or len(tld) > 6 or not tld.isalpha():
                return False

            # Common TLDs list - reject if TLD is not in common list or too long
            # This helps catch malformed emails like "info@domain.comloginlogin"
            common_tlds = {
                'com', 'org', 'net', 'edu', 'gov', 'mil', 'int',
                'it', 'de', 'fr', 'uk', 'us', 'ca', 'au', 'jp', 'cn', 'in', 'br', 'ru', 'es', 'nl', 'be', 'ch', 'se', 'no', 'dk', 'fi', 'pl', 'cz', 'at', 'gr', 'pt', 'ie', 'nz', 'za', 'mx', 'ar', 'cl', 'co', 'pe', 've', 'th', 'sg', 'my', 'ph', 'id', 'vn', 'kr', 'tw', 'hk', 'ae', 'sa', 'il', 'tr', 'eg', 'ng', 'ke', 'gh', 'tz', 'ug', 'et', 'ma', 'tn', 'dz', 'ly', 'sd', 'pk', 'bd', 'lk', 'mm', 'kh', 'la', 'ua', 'by', 'kz', 'uz', 'tm', 'kg', 'ge', 'az', 'am', 'md', 'ro', 'bg', 'hr', 'si', 'sk', 'hu', 'lt', 'lv', 'ee', 'is', 'lu', 'mt', 'cy', 'biz', 'info', 'mobi', 'name', 'pro', 'tel', 'travel', 'xxx', 'asia', 'cat', 'jobs', 'post', 'aero', 'coop', 'museum', 'arpa', 'root', 'local', 'localhost', 'example', 'invalid', 'test'
            }

            if tld.lower() not in common_tlds:
                # If not in common list, still allow if it's a valid 2-6 char TLD
                # But reject if it looks like concatenated text (e.g., "comloginlogin")
                if len(tld) > 6 or any(word in tld.lower() for word in ['login', 'indirizzo', 'napoli', 'roma', 'milano', 'via', 'corso', 'piazza', 'viale']):
                    return False

            return True

        except Exception:
            return False
