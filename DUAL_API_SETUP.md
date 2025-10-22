# Dual API System Setup Guide

## Overview

The scraper now supports **dual Google Maps API keys** with intelligent management:

- **API 1 & API 2**: Each with 11,000 requests/month (free tier limit)
- **Total Capacity**: 22,000 requests/month combined
- **Daily Email Limit**: 500 emails/day (stops and resumes next day)
- **Auto-Switching**: Automatically switches between APIs when one reaches monthly limit
- **Real-time Tracking**: Monitors usage and displays status

## Setup Instructions

### 1. Add Second API Key to .env

Edit your `.env` file and add the second API key:

```env
GOOGLE_MAPS_API_KEY=AIzaSyBy4bf12m69ib1-A1nQ4VyDrHF5JKb6SJw
GOOGLE_MAPS_API_KEY2=AIzaSyBy4bf12m69ib1-A1nQ4VyDrHF5JKb6SJw
```

### 2. Verify Configuration

The system will validate both API keys on startup:

```
✅ API Key 1 initialized successfully
✅ API Key 2 initialized successfully
```

## How It Works

### Daily Email Limit (500 emails)

When the scraper finds 500 emails in a day:
1. ⏸️ Scraping stops automatically
2. ⏳ System waits until midnight
3. 🔄 Resumes scraping the next day
4. 📊 Counter resets to 0

**Logs show:**
```
⏸️  Daily email limit (500) reached! Waiting until tomorrow...
⏳ Sleeping for 8.5 hours until next day...
```

### Monthly Request Limit (11K per API)

Each API tracks monthly requests:
- **API 1**: 0 - 11,000 requests/month
- **API 2**: 0 - 11,000 requests/month

When API 1 reaches 11,000:
1. 🔄 Automatically switches to API 2
2. 📊 Continues scraping with API 2
3. ✅ No interruption to scraping

**Logs show:**
```
⚠️  API 1 monthly limit reached (11000 requests)
🔄 Switched to API 2
```

### Auto-Switching Between APIs

The system intelligently switches APIs:
- Uses API 1 by default
- When API 1 reaches 11K requests → switches to API 2
- When API 2 reaches 11K requests → switches back to API 1
- If both reach limit → stops and shows error

**Logs show:**
```
🔄 Switched to API 2
Current API: 2
```

## API Usage Status

On startup, the system displays current usage:

```
╔════════════════════════════════════════════════════════════════╗
║                    API USAGE STATUS                            ║
╠════════════════════════════════════════════════════════════════╣
║ API 1:                                                         ║
║   Daily Requests:   1234 / ∞                                  ║
║   Monthly Requests: 5678 / 11000                          ║
║                                                                ║
║ API 2:                                                         ║
║   Daily Requests:   2345 / ∞                                  ║
║   Monthly Requests: 3456 / 11000                          ║
║                                                                ║
║ Emails Found Today: 250 / 500                          ║
║ Current API:        1                                                    ║
╚════════════════════════════════════════════════════════════════╝
```

## Usage Tracking

All usage is tracked in `output/api_usage.json`:

```json
{
  "api_1": {
    "daily_requests": 1234,
    "monthly_requests": 5678,
    "last_date": "2025-10-22",
    "last_month": "2025-10"
  },
  "api_2": {
    "daily_requests": 2345,
    "monthly_requests": 3456,
    "last_date": "2025-10-22",
    "last_month": "2025-10"
  },
  "daily_emails": 250,
  "last_email_date": "2025-10-22"
}
```

## Running the Scraper

### Start with Dual API System

```bash
python run_scraper_and_sender.py
```

The system will:
1. ✅ Initialize both API keys
2. 📊 Display current usage status
3. 🔄 Start scraping with API 1
4. 📧 Send emails as they're found
5. 🔄 Auto-switch APIs when needed
6. ⏸️ Stop at 500 emails/day

### Monitor Usage

Check `output/api_usage.json` to see current usage:

```bash
cat output/api_usage.json
```

## Limits Summary

| Metric | Limit | Notes |
|--------|-------|-------|
| API 1 Monthly Requests | 11,000 | Free tier limit |
| API 2 Monthly Requests | 11,000 | Free tier limit |
| **Total Monthly** | **22,000** | Combined capacity |
| Daily Emails | 500 | Stops and resumes next day |
| Daily Requests per API | Unlimited | Only monthly limit applies |

## Expected Performance

With 22,000 total requests/month:
- **Emails per request**: ~1-2 emails (varies by niche)
- **Expected emails/month**: 11,000 - 22,000 emails
- **Daily target**: 500 emails/day
- **Days to reach 500**: ~1 day with good niches

## Troubleshooting

### "Both APIs have reached monthly limit!"

This means both APIs have used 11,000 requests each. Solutions:
1. Wait until next month (limits reset)
2. Add more API keys
3. Reduce search scope

### API Key Not Found

Make sure `.env` has both keys:
```env
GOOGLE_MAPS_API_KEY=your_key_1
GOOGLE_MAPS_API_KEY2=your_key_2
```

### Scraper Stops at 500 Emails

This is expected! The system:
1. Stops scraping at 500 emails
2. Waits until midnight
3. Resumes automatically next day

## Configuration

Edit `config.py` to adjust limits:

```python
max_monthly_requests_per_api: int = 11000  # Free tier limit
max_daily_emails: int = 500  # Stop scraping after 500 emails
```

## Next Steps

1. ✅ Add both API keys to `.env`
2. ✅ Run `python run_scraper_and_sender.py`
3. ✅ Monitor `output/api_usage.json`
4. ✅ Check logs for API switching events
5. ✅ Emails will be sent automatically

---

**Total Capacity**: 22,000 requests/month = ~500 emails/day 🚀

