# 🚀 FREE Google Maps Business Scraper + Email Sender

**100% FREE** Google Maps scraper for Italian travel agencies with automated email sending.

## ✨ Features

✅ **100% FREE** - No API costs using SeleniumBase UC Mode
✅ **Smart Email Extraction** - Dual method: Google Maps + Website scraping
✅ **Automated Email Sending** - Send up to 400 emails/day via Gmail
✅ **Duplicate Protection** - Automatic deduplication of emails
✅ **Rate Limiting** - Safe scraping (10 req/min, 5,000/day)
✅ **Progress Tracking** - Resume from where you left off
✅ **24h Auto-Wait** - Automatically waits when Gmail limit is hit
✅ **Daily Logging** - Comprehensive daily summaries

## 📊 Current Setup

**Keywords:** 446 travel agency keywords
- 214 general agency types (all specializations)
- 232 London-specific keywords (tours, study, entertainment)

**Locations:** 237 Italian cities

**Total Searches:** 105,702 keyword+location combinations

**Language:** Perfect mix of Italian and English (~50/50)

## 🎯 What You'll Find

✅ General travel agencies (all types)
✅ London travel specialists
✅ Study abroad agencies (English courses)
✅ Educational travel providers
✅ Event & MICE agencies
✅ Wedding & honeymoon specialists
✅ Transfer & support services

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure Email (First Time Only)

The scraper will ask for your Gmail credentials on first run:
- Gmail address
- Gmail App Password ([How to get it](https://support.google.com/accounts/answer/185833))
- Email subject
- Email message

Configuration is saved to `email_config.json` for future runs.

### 3️⃣ Run the Scraper + Email Sender

```bash
python run_free_scraper.py
```

This will:
1. **Scraper**: Search Google Maps and extract emails (10 searches/min)
2. **Email Sender**: Send emails to collected addresses (400/day max)
3. Both run in parallel automatically

### 4️⃣ Monitor Progress

**Real-time console output:**
```
Scraper: 1,234/105,702 searches (1.2%) | 567 businesses | 89 emails
Email Sender: 45/89 sent (50.6%) | 2 failed | Next: 24h wait at limit
```

**Detailed logs:**
```bash
# Scraper logs
tail -f logs/scraper.log

# Email sender logs
tail -f logs/email_sender.log

# Runner logs
tail -f logs/runner.log
```

## 📁 Project Structure

```
gmaps_bot_api_version/
├── input/
│   ├── niches.csv              # 446 keywords (general + London)
│   └── locations.csv           # 237 Italian cities
├── output/
│   ├── scraped_data.csv        # All scraped businesses
│   └── progress.json           # Scraper progress tracking
├── logs/
│   ├── scraper.log            # Scraper detailed logs
│   ├── email_sender.log       # Email sender detailed logs
│   └── runner.log             # Main runner logs
├── emails.json                 # Email database (unique, deduplicated)
├── email_config.json          # Email configuration (auto-created)
├── run_free_scraper.py        # Main runner (START HERE)
├── seleniumbase_scraper.py    # FREE scraper (SeleniumBase UC Mode)
├── simple_email_sender.py     # Email sender (Gmail SMTP)
├── simple_email_manager.py    # Email manager (deduplication)
├── email_scraper.py           # Email extraction from websites
├── rate_limiter.py            # Rate limiting (10/min, 5000/day)
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 📊 Data Flow

```
1. SCRAPING:
   niches.csv + locations.csv
   → seleniumbase_scraper.py (Google Maps search)
   → email_scraper.py (extract emails from websites)
   → output/scraped_data.csv (all businesses)
   → emails.json (unique emails only)

2. EMAIL SENDING:
   emails.json (unique, unsent emails)
   → simple_email_sender.py (Gmail SMTP)
   → emails.json (updated with sent status)
```

## ⚙️ Configuration

### Rate Limiting (Automatic)
- **10 searches/minute** (6 sec intervals)
- **300 searches/hour**
- **5,000 searches/day**
- Prevents IP blocking

### Email Limits (Automatic)
- **400 emails/day** (Gmail limit)
- **3 seconds between emails**
- **24h auto-wait** when limit hit
- Resumes automatically after 24h

### Customization

Edit `config.py` to change scraper settings:
```python
# Search settings
max_results_per_search: int = 200
search_radius: int = 50000  # meters

# Email scraping
enable_email_scraping: bool = True
website_timeout: int = 10  # seconds
max_pages_per_website: int = 3
```

Edit `simple_email_sender.py` to change email settings:
```python
self.daily_limit = 400  # emails per day
self.delay_between_emails = 3  # seconds
```

## 🔄 Progress Tracking

### Scraper Progress
Saved in `output/progress.json`:
```json
{
  "current_niche_index": 45,
  "current_location_index": 123
}
```

**To reset and start fresh:**
```bash
python -c "import json; json.dump({'current_niche_index': 0, 'current_location_index': 0}, open('output/progress.json', 'w'))"
```

### Email Database
Saved in `emails.json`:
```json
{
  "all_emails": {
    "info@example.com": {
      "business_name": "Agenzia Viaggi Roma",
      "sent_count": 1,
      "last_sent": "2025-11-14 10:30:45"
    }
  },
  "stats": {
    "total_collected": 771,
    "total_sent": 362,
    "total_failed": 87
  }
}
```

## 📈 Expected Results

**Estimated Timeline:**
- **Total searches:** 105,702
- **At 10 searches/min:** ~176 hours (~7 days)
- **Emails collected:** 10,000-15,000
- **Emails sent:** 400/day

**What You'll Get:**
- ✅ 10,000-15,000 unique email addresses
- ✅ Travel agencies across all 237 Italian cities
- ✅ General agencies + London specialists
- ✅ Study abroad agencies
- ✅ Event & MICE agencies
- ✅ Wedding & honeymoon specialists

## 🚨 Troubleshooting

### Scraper Issues

**"No businesses found"**
- Normal for some keyword+location combinations
- Scraper will continue to next search

**"Rate limit exceeded"**
- Automatic wait and retry
- This is normal and expected

**"Email extraction failed"**
- Normal - not all websites have emails
- Scraper tries Google Maps first, then website

### Email Sender Issues

**"Daily user sending limit exceeded"**
- Gmail limit hit (400 emails/day)
- Sender will automatically wait 24h
- Resumes automatically after wait period

**"Authentication failed"**
- Check Gmail App Password
- Make sure 2FA is enabled on Gmail
- Regenerate App Password if needed

**"No unsent emails"**
- All collected emails have been sent
- Wait for scraper to collect more emails

### General Issues

**"Process crashed"**
- Simply run `python run_free_scraper.py` again
- Progress is automatically saved
- Will resume from where it left off

**"Duplicate emails"**
- Automatic deduplication in `emails.json`
- Each email sent only once
- No manual cleanup needed

## 🎯 Tips for Best Results

1. **Let it run continuously** - Both scraper and sender run 24/7
2. **Monitor logs** - Check daily summaries in log files
3. **Don't reset progress** - Unless you want to start over
4. **Backup emails.json** - Contains all your collected emails
5. **Check Gmail quota** - Make sure you're not hitting other limits

## 🔒 Safety Features

✅ **Rate Limiting** - Prevents IP bans (10/min, 5000/day)
✅ **Duplicate Protection** - Each email sent only once
✅ **24h Auto-Wait** - Automatic Gmail limit handling
✅ **Progress Tracking** - Never lose your work
✅ **Error Handling** - Graceful failure recovery
✅ **Daily Logging** - Comprehensive daily summaries

## 📊 Current Status

**Keywords:** 446 total
- General agencies: 214 keywords
- London specialists: 232 keywords

**Locations:** 237 Italian cities

**Search Combinations:** 105,702 total

**Language Mix:** ~50% Italian, ~50% English

## 🎉 Success Metrics

After running for a few days, you should see:
- ✅ Thousands of businesses scraped
- ✅ Thousands of unique emails collected
- ✅ Hundreds of emails sent daily (up to 400/day)
- ✅ Detailed logs for analysis
- ✅ Automatic progress tracking

**Happy scraping! 🚀**
