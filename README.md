# Google Maps Business Scraper

A robust, production-ready Google Maps scraper that can run continuously overnight to extract business information for multiple niches and locations.

## Features

✅ **Continuous Operation**: Runs overnight safely without getting banned  
✅ **Crash Recovery**: Automatically recovers data if the script or computer crashes  
✅ **Duplicate Removal**: Removes duplicates based on phone numbers  
✅ **Rate Limiting**: Built-in safety measures to avoid API bans  
✅ **Progress Tracking**: Resumes from where it left off  
✅ **Configurable**: Easy to adjust for Google Maps changes  
✅ **Comprehensive Logging**: Detailed logs for monitoring and debugging  

## Data Extracted

- Business name
- Niche/category
- Full address
- State
- Phone number
- Website
- Google Maps result URL

*Note: If any information is not available, "NOT AVAILABLE" is recorded*

## 🚀 Quick Start

### 📋 **STEP 1: Get Detailed Setup Instructions**

**For complete API setup with screenshots and every detail:**
👉 **Read: `API_SETUP_INSTRUCTIONS.txt`** 👈

**For step-by-step running instructions:**
👉 **Read: `HOW_TO_RUN_SCRAPER.txt`** 👈

### ⚡ **STEP 2: Quick Setup**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Google Maps API Key** (detailed steps in `API_SETUP_INSTRUCTIONS.txt`):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable Places API → Create API Key
   - Secure your API key with IP restrictions

3. **Add API Key to scraper:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and replace `your_api_key_here` with your actual API key
   - Example: `GOOGLE_MAPS_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 🎯 **STEP 3: Test & Run**

**Test first:**
```bash
python main.py --mode single --niche "roofers" --location "San Diego, CA"
```

**Run full scraper:**
```bash
python main.py --mode continuous
```

**Windows users:** Double-click `run_scraper.bat` for easy menu interface!

### 4. Customize Input Data

Edit the input files to match your needs:

- `input/niches.csv`: Add your target business niches
- `input/locations.csv`: Add your target cities and states

## Usage

### Continuous Scraping (Recommended)

Run the scraper continuously for all niches and locations:

```bash
python main.py --mode continuous
```

This will:
- Process all niche/location combinations
- Save data continuously
- Handle crashes and resume automatically
- Run safely overnight

### Single Search (Testing)

Test with a single niche and location:

```bash
python main.py --mode single --niche "roofers" --location "San Diego, CA"
```

### Cleanup Only

Remove duplicates from existing data:

```bash
python main.py --mode cleanup
```

## Configuration

Adjust settings in `config.py`:

- **Rate Limiting**: `requests_per_minute`, `delay_between_requests`
- **Safety**: `max_daily_requests`, `max_retries`
- **Data**: `max_results_per_search`, `backup_interval`

## File Structure

```
├── main.py              # Main runner script
├── scraper.py           # Core scraper logic
├── data_manager.py      # Data persistence and recovery
├── config.py            # Configuration settings
├── test_scraper.py      # Test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── input/
│   ├── niches.csv       # Target business niches
│   └── locations.csv    # Target cities and states
├── output/
│   ├── scraped_data.csv # Raw scraped data
│   ├── scraped_data_final.csv # Clean data (no duplicates)
│   ├── temp_scraped_data.csv  # Temporary file for crash recovery
│   └── progress.json    # Progress tracking
├── logs/
│   └── scraper.log      # Detailed logs
└── backups/             # Automatic backups
```

## Safety Features

### Anti-Ban Protection
- Rate limiting (30 requests/minute by default)
- Random delays between requests
- Daily request limits
- Retry logic with exponential backoff

### Crash Recovery
- Progress is saved after each location
- Temporary files store data continuously
- Automatic recovery on restart
- Regular backups

### Error Handling
- Graceful handling of API errors
- Skips problematic locations/niches
- Comprehensive logging
- Continues operation despite individual failures

## Testing

Run the test suite:

```bash
python test_scraper.py
```

This will run:
1. Unit tests (no API calls required)
2. Integration test (requires valid API key)

## Monitoring

### Check Progress
Monitor the scraper through:
- Console output (real-time)
- Log file: `logs/scraper.log`
- Progress file: `output/progress.json`

### Data Statistics
The scraper provides detailed statistics:
- Total records scraped
- Unique businesses found
- Coverage by niche and location
- Duplicate removal results

## Troubleshooting

### Common Issues

**"Google Maps API key not found"**
- Ensure your `.env` file contains the correct API key
- Verify the API key has proper permissions

**"No results found"**
- Check if the niche/location combination is valid
- Verify your API key has sufficient quota
- Try a different search term

**"Rate limit exceeded"**
- The scraper will automatically wait and retry
- Adjust `requests_per_minute` in config.py if needed

### Adjusting for Google Maps Changes

If Google Maps changes and breaks the scraper:

1. Check the logs for specific error messages
2. Update the field mappings in `_extract_business_data()` method
3. Adjust the search parameters in `_search_places()` method
4. Test with single searches before running continuously

## Best Practices

1. **Start Small**: Test with a few niches/locations first
2. **Monitor Logs**: Keep an eye on the log file during operation
3. **Regular Backups**: The system creates automatic backups, but consider additional backups for important data
4. **API Quota**: Monitor your Google Maps API usage in Google Cloud Console
5. **Respectful Scraping**: Don't increase rate limits too aggressively

## Support

For issues or questions:
1. Check the log files for error details
2. Run the test suite to verify setup
3. Review the configuration settings
4. Ensure your Google Maps API key is properly configured
