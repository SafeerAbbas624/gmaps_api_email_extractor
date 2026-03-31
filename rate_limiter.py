"""
Rate Limiter for Google Maps Scraping
Prevents IP blocking by limiting requests per minute/hour/day
"""

import time
import random
import logging
from datetime import datetime, timedelta
from typing import Optional


class RateLimiter:
    """
    Rate limiter to prevent IP blocking
    
    Limits:
    - 10 requests per minute (1 every 6 seconds)
    - 300 requests per hour
    - 5,000 requests per day
    """
    
    def __init__(
        self,
        requests_per_minute: int = 10,
        requests_per_hour: int = 300,
        requests_per_day: int = 5000,
        min_delay: float = 2.0,
        max_delay: float = 5.0
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        self.min_delay = min_delay
        self.max_delay = max_delay
        
        # Counters
        self.minute_count = 0
        self.hour_count = 0
        self.day_count = 0
        
        # Timestamps
        self.last_minute = time.time()
        self.last_hour = time.time()
        self.last_day = time.time()
        self.last_request = time.time()
        
        # Logger
        self.logger = logging.getLogger('rate_limiter')
    
    def wait_if_needed(self):
        """
        Wait if rate limits are reached
        Also adds random delays to appear human-like
        """
        current_time = time.time()
        
        # Reset counters if time windows have passed
        self._reset_counters(current_time)
        
        # Check daily limit
        if self.day_count >= self.requests_per_day:
            self._wait_until_next_day(current_time)
            return
        
        # Check hourly limit
        if self.hour_count >= self.requests_per_hour:
            self._wait_until_next_hour(current_time)
            return
        
        # Check minute limit
        if self.minute_count >= self.requests_per_minute:
            self._wait_until_next_minute(current_time)
            return
        
        # Add random delay between requests (human-like behavior)
        time_since_last = current_time - self.last_request
        min_wait = self.min_delay
        
        if time_since_last < min_wait:
            wait_time = min_wait - time_since_last
            random_extra = random.uniform(0, self.max_delay - self.min_delay)
            total_wait = wait_time + random_extra
            
            self.logger.info(f"⏳ Waiting {total_wait:.1f}s (human-like delay)")
            time.sleep(total_wait)
        else:
            # Still add a small random delay
            random_delay = random.uniform(self.min_delay, self.max_delay)
            self.logger.info(f"⏳ Random delay: {random_delay:.1f}s")
            time.sleep(random_delay)
        
        # Increment counters
        self.minute_count += 1
        self.hour_count += 1
        self.day_count += 1
        self.last_request = time.time()
        
        # Log current status
        self._log_status()
    
    def _reset_counters(self, current_time: float):
        """Reset counters if time windows have passed"""
        # Reset minute counter
        if current_time - self.last_minute > 60:
            self.minute_count = 0
            self.last_minute = current_time
        
        # Reset hour counter
        if current_time - self.last_hour > 3600:
            self.hour_count = 0
            self.last_hour = current_time
        
        # Reset day counter
        if current_time - self.last_day > 86400:
            self.day_count = 0
            self.last_day = current_time
    
    def _wait_until_next_minute(self, current_time: float):
        """Wait until next minute"""
        wait_time = 60 - (current_time - self.last_minute)
        self.logger.warning(
            f"⏸️ MINUTE LIMIT REACHED ({self.minute_count}/{self.requests_per_minute})"
        )
        self.logger.info(f"⏳ Waiting {wait_time:.1f}s until next minute...")
        time.sleep(wait_time)
        self.minute_count = 0
        self.last_minute = time.time()
    
    def _wait_until_next_hour(self, current_time: float):
        """Wait until next hour"""
        wait_time = 3600 - (current_time - self.last_hour)
        self.logger.warning(
            f"⏸️ HOUR LIMIT REACHED ({self.hour_count}/{self.requests_per_hour})"
        )
        self.logger.info(f"⏳ Waiting {wait_time/60:.1f} minutes until next hour...")
        time.sleep(wait_time)
        self.hour_count = 0
        self.last_hour = time.time()
    
    def _wait_until_next_day(self, current_time: float):
        """Wait until next day"""
        wait_time = 86400 - (current_time - self.last_day)
        self.logger.warning(
            f"⏸️ DAILY LIMIT REACHED ({self.day_count}/{self.requests_per_day})"
        )
        self.logger.info(f"⏳ Waiting {wait_time/3600:.1f} hours until next day...")
        
        # Calculate exact reset time
        reset_time = datetime.now() + timedelta(seconds=wait_time)
        self.logger.info(f"📅 Will resume at: {reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        time.sleep(wait_time)
        self.day_count = 0
        self.last_day = time.time()
    
    def _log_status(self):
        """Log current rate limit status"""
        self.logger.info(
            f"📊 Rate Status: "
            f"Minute: {self.minute_count}/{self.requests_per_minute} | "
            f"Hour: {self.hour_count}/{self.requests_per_hour} | "
            f"Day: {self.day_count}/{self.requests_per_day}"
        )
    
    def get_status(self) -> dict:
        """Get current rate limit status"""
        return {
            'minute': {
                'current': self.minute_count,
                'limit': self.requests_per_minute,
                'remaining': self.requests_per_minute - self.minute_count
            },
            'hour': {
                'current': self.hour_count,
                'limit': self.requests_per_hour,
                'remaining': self.requests_per_hour - self.hour_count
            },
            'day': {
                'current': self.day_count,
                'limit': self.requests_per_day,
                'remaining': self.requests_per_day - self.day_count
            }
        }

    def get_wait_time(self) -> float:
        """
        Get the wait time needed before next request (without actually waiting).
        Returns 0 if no wait is needed.
        """
        current_time = time.time()

        # Reset counters if time windows have passed
        self._reset_counters(current_time)

        # Check daily limit
        if self.day_count >= self.requests_per_day:
            wait_time = 86400 - (current_time - self.last_day)
            self.logger.warning(
                f"⏸️ DAILY LIMIT REACHED ({self.day_count}/{self.requests_per_day})"
            )
            return wait_time

        # Check hourly limit
        if self.hour_count >= self.requests_per_hour:
            wait_time = 3600 - (current_time - self.last_hour)
            self.logger.warning(
                f"⏸️ HOUR LIMIT REACHED ({self.hour_count}/{self.requests_per_hour})"
            )
            return wait_time

        # Check minute limit
        if self.minute_count >= self.requests_per_minute:
            wait_time = 60 - (current_time - self.last_minute)
            self.logger.warning(
                f"⏸️ MINUTE LIMIT REACHED ({self.minute_count}/{self.requests_per_minute})"
            )
            return wait_time

        return 0  # No wait needed

    def record_request(self):
        """
        Record that a request was made (increment counters).
        Call this after completing a wait via get_wait_time().
        """
        current_time = time.time()

        # Reset counters if time windows have passed
        self._reset_counters(current_time)

        # Increment counters
        self.minute_count += 1
        self.hour_count += 1
        self.day_count += 1
        self.last_request = time.time()

        # Log current status
        self._log_status()

    def reset_all(self):
        """Reset all counters (for testing)"""
        self.minute_count = 0
        self.hour_count = 0
        self.day_count = 0
        self.last_minute = time.time()
        self.last_hour = time.time()
        self.last_day = time.time()
        self.logger.info("🔄 All rate limit counters reset")
    
    def add_human_behavior(self):
        """Add random human-like behaviors"""
        behaviors = [
            self._random_pause,
            self._random_short_delay,
            self._random_long_delay
        ]
        
        # 30% chance to add extra human behavior
        if random.random() < 0.3:
            behavior = random.choice(behaviors)
            behavior()
    
    def _random_pause(self):
        """Random short pause (like reading)"""
        pause = random.uniform(0.5, 1.5)
        self.logger.debug(f"👤 Human behavior: Reading pause ({pause:.1f}s)")
        time.sleep(pause)
    
    def _random_short_delay(self):
        """Random short delay (like thinking)"""
        delay = random.uniform(1.0, 3.0)
        self.logger.debug(f"👤 Human behavior: Thinking delay ({delay:.1f}s)")
        time.sleep(delay)
    
    def _random_long_delay(self):
        """Random long delay (like taking a break)"""
        delay = random.uniform(5.0, 10.0)
        self.logger.debug(f"👤 Human behavior: Break ({delay:.1f}s)")
        time.sleep(delay)


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create rate limiter
    limiter = RateLimiter()
    
    # Simulate requests
    print("Testing rate limiter...")
    for i in range(15):
        print(f"\n--- Request {i+1} ---")
        limiter.wait_if_needed()
        print(f"✅ Request {i+1} completed")
        print(f"Status: {limiter.get_status()}")

