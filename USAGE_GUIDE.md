# Google Maps Scraper - Complete Usage Guide

## Quick Start

### 1. First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your Google Maps API key

# Run setup (optional)
python setup.py
```

### 2. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable these APIs:
   - Places API
   - Maps JavaScript API
4. Create an API Key
5. **Important**: Restrict your API key to your IP address for security
6. Add the key to your `.env` file

### 3. Customize Your Data

Edit these files with your target data:

**input/niches.csv**
```csv
niche
roofers
plumbers
electricians
your_niche_here
```

**input/locations.csv**
```csv
city,state
San Diego,CA
Los Angeles,CA
Your City,ST
```

## Running the Scraper

### Test First (Recommended)

```bash
# Test with a single search
python main.py --mode single --niche "roofers" --location "San Diego, CA"
```

### Continuous Scraping

```bash
# Run for all niches and locations
python main.py --mode continuous
```

**This will:**
- Process every niche/location combination
- Save data continuously (crash-safe)
- Resume automatically if interrupted
- Run safely overnight
- Respect rate limits to avoid bans

### Clean Data

```bash
# Remove duplicates from scraped data
python main.py --mode cleanup
```

## Monitoring and Management

### Check Progress

```bash
python utils.py progress
```

### View Statistics

```bash
python utils.py stats
```

### Create Manual Backup

```bash
python utils.py backup
```

### Reset Progress (Start Over)

```bash
python utils.py reset
```

## Safety Features

### Rate Limiting
- **30 requests per minute** (configurable)
- **2 second delay** between requests
- **2000 daily request limit** (configurable)
- Automatic retry with exponential backoff

### Crash Recovery
- Progress saved after each location
- Temporary files for data recovery
- Automatic backups every 100 records
- Resume from exact stopping point

### Error Handling
- Graceful handling of API errors
- Skips problematic searches
- Continues despite individual failures
- Comprehensive logging

## Output Files

### Main Files
- `output/scraped_data.csv` - Raw scraped data
- `output/scraped_data_final.csv` - Clean data (no duplicates)
- `output/progress.json` - Current progress
- `logs/scraper.log` - Detailed logs

### Backup Files
- `backups/` - Automatic timestamped backups
- `output/temp_scraped_data.csv` - Crash recovery file

## Customization

### Adjusting for Google Maps Changes

If Google Maps changes and breaks the scraper:

1. **Check logs** for specific errors
2. **Update field mappings** in `scraper.py`:
   ```python
   def _extract_business_data(self, place, niche, location):
       # Modify field extraction here
   ```
3. **Adjust search parameters** in `config.py`:
   ```python
   max_results_per_search = 20  # Reduce if getting errors
   delay_between_requests = 3.0  # Increase if rate limited
   ```

### Configuration Options

Edit `config.py` to customize:

```python
# Rate limiting
requests_per_minute = 30        # Requests per minute
delay_between_requests = 2.0    # Seconds between requests
max_daily_requests = 2000       # Daily limit

# Search settings
max_results_per_search = 20     # Results per search
search_radius = 50000           # Search radius in meters

# Safety settings
max_retries = 3                 # Retry attempts
retry_delay = 5.0               # Retry delay
backup_interval = 100           # Backup every N records
```

## Troubleshooting

### Common Issues

**"API key not found"**
- Check your `.env` file
- Ensure API key is correct
- Verify API permissions in Google Cloud

**"No results found"**
- Try different search terms
- Check if location exists
- Verify API quota

**"Rate limit exceeded"**
- Scraper will automatically wait and retry
- Reduce `requests_per_minute` if needed

**"Script stops unexpectedly"**
- Check `logs/scraper.log` for errors
- Run with `--mode continuous` to auto-resume
- Use crash recovery features

### Getting Help

1. Check `logs/scraper.log` for detailed error messages
2. Run `python utils.py stats` to see current data status
3. Test with single searches first: `python main.py --mode single --niche "test" --location "Test City, ST"`

## Best Practices

### For Long-Term Use

1. **Start small** - Test with a few niches/locations first
2. **Monitor logs** - Keep an eye on the log file
3. **Regular backups** - Use `python utils.py backup`
4. **Check API usage** - Monitor in Google Cloud Console
5. **Respectful scraping** - Don't increase rate limits too aggressively

### Overnight Operation

The scraper is designed to run safely overnight:
- Automatic rate limiting prevents bans
- Crash recovery ensures no data loss
- Progress tracking allows resuming
- Graceful shutdown on interruption

### Data Quality

- Phone numbers are used for duplicate detection
- "NOT AVAILABLE" is used for missing data
- State extraction handles various address formats
- All Google Maps URLs are preserved for verification

## Advanced Usage

### Custom Data Fields

To scrape additional fields, modify `config.py`:

```python
data_fields = [
    "name", "niche", "address", "state", 
    "phone_number", "website", "result_url",
    "rating", "review_count"  # Add custom fields
]
```

Then update the extraction logic in `scraper.py`.

### Batch Processing

For very large datasets:
1. Split your locations into smaller files
2. Run multiple instances with different input files
3. Combine results using the cleanup function

### Integration

The scraper can be integrated into larger workflows:
- Import `GoogleMapsScraper` class
- Use `scrape_niche_location()` method
- Handle data with `DataManager` class
