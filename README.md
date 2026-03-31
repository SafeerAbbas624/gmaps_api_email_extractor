# Google Maps Business Scraper + Automated Email Sender

A fully automated pipeline that scrapes business contact information from Google Maps, extracts emails from business websites, and sends personalized outreach emails — all for free using SeleniumBase (no Google Maps API required).

---

## Table of Contents

- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [File Reference](#file-reference)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [1. Target Audience — niches.csv and locations.csv](#1-target-audience--nichescsv-and-locationscsv)
  - [2. Email Templates — email_messages.py](#2-email-templates--email_messagespy)
  - [3. Gmail Credentials — email_config.json](#3-gmail-credentials--email_configjson)
  - [4. Bot Behavior — bot_settings.json](#4-bot-behavior--bot_settingsjson)
  - [5. Scraper Settings — config.py](#5-scraper-settings--configpy)
- [Running the Bot](#running-the-bot)
- [Monitoring Progress](#monitoring-progress)
- [Email Preview System](#email-preview-system)
- [Output Files](#output-files)
- [Resetting Progress](#resetting-progress)
- [Troubleshooting](#troubleshooting)
- [Safety and Limits](#safety-and-limits)

---

## How It Works

```
input/niches.csv  +  input/locations.csv
         |
         v
  seleniumbase_scraper.py
  (searches Google Maps for each keyword + location combination)
         |
         v
  email_scraper.py
  (visits each business website and extracts email addresses)
         |
         v
  emails.json  +  output/scraped_data.csv
  (deduplicated email database + full business records)
         |
         v
  simple_email_sender.py
  (sends your email templates to collected addresses via Gmail SMTP)
```

Both the scraper and the email sender run **in parallel** from a single command. The scraper collects emails while the sender works through the queue simultaneously.

---

## Project Structure

```
gmaps_bot_api_version/
│
├── input/
│   ├── niches.csv              # Keywords to search on Google Maps (one per line)
│   └── locations.csv           # Cities/locations to search in (city, state columns)
│
├── output/
│   ├── scraped_data.csv        # Every business scraped (name, address, phone, email, URL)
│   └── progress.json           # Tracks which keyword+location the scraper is up to
│
├── logs/
│   ├── scraper.log             # Detailed scraper activity log
│   ├── email_sender.log        # Email sending activity log
│   └── runner.log              # Main runner log
│
├── downloaded_files/           # Files downloaded during scraping (attachments etc.)
│
├── run_free_scraper.py         # MAIN ENTRY POINT — run this to start everything
├── seleniumbase_scraper.py     # Google Maps scraper (FREE, no API key needed)
├── email_scraper.py            # Extracts emails from business websites
├── simple_email_sender.py      # Sends emails via Gmail SMTP
├── simple_email_manager.py     # Manages the email database (deduplication, tracking)
├── rate_limiter.py             # Prevents IP bans (limits requests per minute/hour/day)
│
├── email_messages.py           # YOUR EMAIL TEMPLATES — edit this to change what is sent
├── email_config.json           # Gmail credentials and default subject/message
├── email_preview.html          # Visual HTML preview of all email templates (auto-generated)
├── generate_preview.py         # Regenerates email_preview.html from email_messages.py
├── check_messages.py           # Quick script to print all message subjects to console
├── create_email_messages.py    # Helper script to regenerate email_messages.py from scratch
│
├── bot_settings.json           # Bot scheduling settings (start time, daily limit, delays)
├── bot_settings.py             # Settings manager class (reads/writes bot_settings.json)
├── config.py                   # Scraper configuration (API keys, rate limits, file paths)
│
├── emails.json                 # Email database — every collected and sent email is tracked here
├── requirements.txt            # Python package dependencies
└── .env                        # (create this yourself) Google Maps API keys if you want API mode
```

---

## File Reference

### Files You Will Edit Regularly

| File | What to change |
|------|---------------|
| `input/niches.csv` | The keywords (business types) to search for on Google Maps |
| `input/locations.csv` | The cities and states/regions to search in |
| `email_messages.py` | Your outreach email subject lines, plain text body, and HTML body |
| `bot_settings.json` | When emails start sending, daily limit, delay between emails, timezone |
| `email_config.json` | Your Gmail address and App Password |

### Files You Should Know About (but rarely edit)

| File | Purpose |
|------|---------|
| `run_free_scraper.py` | Starts the scraper and email sender together. Run this. |
| `config.py` | Advanced scraper tuning: search radius, results per search, timeouts |
| `generate_preview.py` | Regenerates `email_preview.html` after editing `email_messages.py` |
| `check_messages.py` | Prints all message subjects to console for a quick sanity check |
| `create_email_messages.py` | Overwrites `email_messages.py` from a set of messages defined inside it. Edit this if you want to bulk-replace all templates at once. |

### Auto-Generated Files (do not manually edit)

| File | Description |
|------|-------------|
| `emails.json` | Persistent database of all collected emails and their send status |
| `output/scraped_data.csv` | Full record of every scraped business |
| `output/progress.json` | Tracks scraper progress so it can resume after a restart |
| `email_preview.html` | HTML preview of your email templates — regenerated by `generate_preview.py` |
| `logs/` | Log files written automatically |

---

## Prerequisites

- **Python 3.9 or higher**
- **Google Chrome** installed (SeleniumBase manages its own ChromeDriver)
- A **Gmail account** with 2-Factor Authentication enabled
- A **Gmail App Password** (not your regular Gmail password)

### Getting a Gmail App Password

1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security** > **2-Step Verification** (must be enabled first)
3. Scroll to the bottom and click **App passwords**
4. Select **Mail** and **Windows Computer** (or your OS)
5. Click **Generate** — copy the 16-character password
6. Use this password in `email_config.json` (not your real Gmail password)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

SeleniumBase will automatically download and manage the correct ChromeDriver for your Chrome version — no manual setup needed.

---

## Configuration

### 1. Target Audience — `niches.csv` and `locations.csv`

These two files define **what** to search for and **where**.

**`input/niches.csv`** — one keyword per row under the `niche` header:
```
niche
real estate agency
property management
dental clinic
law firm
accounting firm
```
Each keyword is searched in every location, so keep the list focused. 500 keywords × 100 locations = 50,000 searches.

**`input/locations.csv`** — one city per row with `city` and `state` columns:
```
city,state
New York,NY
Los Angeles,CA
Chicago,IL
London,UK
Sydney,NSW
```
The `state` column is optional but helps narrow down results in large countries.

---

### 2. Email Templates — `email_messages.py`

This is the most important file to customize. It contains a list called `EMAIL_MESSAGES` where each entry is one message variation. The bot picks a random one for each email it sends — this helps avoid Gmail spam filters.

**Structure of each message:**
```python
EMAIL_MESSAGES = [
    {
        "subject": "Your email subject line here",
        "plain": """Your plain text email body here.

Can span multiple lines.
""",
        "html": """<html><body>
<p>Your <strong>HTML</strong> email body here.</p>
</body></html>"""
    },
    {
        # Add more variations...
    }
]
```

**Rules:**
- Include at least 3-5 variations to reduce spam detection
- Keep the `plain` and `html` bodies consistent with each other
- The `plain` version is the fallback shown by email clients that do not render HTML
- Do not remove the `get_random_message()` function at the bottom of the file

**After editing `email_messages.py`, regenerate the preview:**
```bash
python generate_preview.py
```
Then open `email_preview.html` in your browser to see exactly how all your emails will look.

**To watch for changes and auto-update the preview:**
```bash
python generate_preview.py --watch
```
Leave this running while you edit `email_messages.py` — the HTML refreshes automatically on every save.

---

### 3. Gmail Credentials — `email_config.json`

Create or edit this file with your Gmail details:

```json
{
  "sender_email": "your.email@gmail.com",
  "sender_password": "xxxx xxxx xxxx xxxx",
  "email_subject": "Default subject (overridden by email_messages.py)",
  "message_content": "Default body (overridden by email_messages.py)"
}
```

- `sender_email` — your full Gmail address
- `sender_password` — the 16-character **App Password** (with or without spaces)
- `email_subject` and `message_content` — legacy fallback fields; the actual content comes from `email_messages.py`

> **Security note:** Never commit `email_config.json` to a public repository. Add it to `.gitignore`.

---

### 4. Bot Behavior — `bot_settings.json`

Controls when and how fast the bot sends emails:

```json
{
  "email_sending_start_time": "09:00",
  "daily_email_limit": 120,
  "delay_between_emails": 600,
  "timezone": "America/New_York"
}
```

| Setting | Description | Example values |
|---------|-------------|----------------|
| `email_sending_start_time` | Time of day to start sending (24-hour HH:MM) | `"09:00"`, `"08:30"` |
| `daily_email_limit` | Maximum emails to send per day | `100`, `200`, `400` |
| `delay_between_emails` | Seconds to wait between each email | `300` (5 min), `600` (10 min) |
| `timezone` | Your local timezone for scheduling | `"America/New_York"`, `"Europe/London"`, `"Asia/Karachi"` |

**Gmail's safe sending limits (to avoid account suspension):**
- New accounts: 50-100 emails/day
- Established accounts (6+ months old): up to 400-500/day
- Keep `delay_between_emails` at 300 seconds (5 minutes) minimum for safety

**Common timezones:**
```
America/New_York      America/Chicago       America/Los_Angeles
America/Toronto       Europe/London         Europe/Berlin
Europe/Paris          Asia/Karachi          Asia/Kolkata
Asia/Dubai            Australia/Sydney
```

You can also change these settings interactively when you run the bot:
```bash
python run_free_scraper.py
# The bot will ask: "Do you want to change any settings? (y/n)"
```

---

### 5. Scraper Settings — `config.py`

Most users do not need to touch this. Advanced settings:

```python
# How many results to fetch per search query
max_results_per_search: int = 200

# Search radius around the location (meters)
search_radius: int = 50000  # 50 km

# How long to wait for a business website to load
website_timeout: int = 10  # seconds

# How many pages of a website to check for emails (home, contact, about)
max_pages_per_website: int = 3

# Enable/disable website email scraping
enable_email_scraping: bool = True
```

**Google Maps API mode (optional):**  
The scraper works 100% free using SeleniumBase by default. If you want to use the official Google Maps API instead (faster but has monthly limits), create a `.env` file:

```
GOOGLE_MAPS_API_KEY=your_api_key_here
GOOGLE_MAPS_API_KEY2=your_second_api_key_here
```

Each free API key gives 11,000 requests/month. The bot automatically rotates between the two keys.

---

## Running the Bot

### Start everything (scraper + email sender in parallel)

```bash
python run_free_scraper.py
```

On first run the bot will:
1. Show current bot settings and ask if you want to change them
2. Ask for your Gmail credentials if `email_config.json` does not exist yet
3. Start the scraper and email sender in parallel

### What happens next

- **Scraper**: Opens a browser window, searches Google Maps for each keyword+location combination, visits business websites to extract emails, and saves everything to `output/scraped_data.csv` and `emails.json`
- **Email sender**: Reads new emails from `emails.json` and sends your templates, respecting the daily limit and start time you configured
- **Progress is saved automatically** — if you stop and restart, it picks up where it left off

### Console output example

```
[Scraper]       Searching: "real estate agency" in "New York, NY"
[Scraper]       Found 23 businesses | Extracted 7 emails
[Email Sender]  Sent to info@example.com (12/100 today)
[Email Sender]  Waiting 600s before next email...
```

---

## Monitoring Progress

### Log files

| File | What it contains |
|------|-----------------|
| `logs/scraper.log` | Every search, business found, email extracted, error |
| `logs/email_sender.log` | Every email sent, failed, daily limit hits |
| `logs/runner.log` | Overall runner status and subprocess management |

On Windows, follow logs in PowerShell:
```powershell
Get-Content logs\scraper.log -Wait -Tail 50
Get-Content logs\email_sender.log -Wait -Tail 50
```

### Email database stats

Open `emails.json` and check the `stats` block:
```json
{
  "stats": {
    "total_collected": 1430,
    "total_sent": 562,
    "total_failed": 23
  },
  "daily_tracking": {
    "date": "2026-03-31",
    "sent_today": 47
  }
}
```

### Quick message check

```bash
python check_messages.py
```
Prints all email template subjects to confirm they loaded correctly.

---

## Email Preview System

Before sending, always preview your emails:

```bash
# One-time generation
python generate_preview.py

# Auto-update whenever you edit email_messages.py
python generate_preview.py --watch
```

Then open `email_preview.html` in any browser. It shows:
- All message variations with their subjects
- HTML rendered version of each email
- Plain text version toggle
- Total count of messages

This is the exact same content recipients will see.

---

## Output Files

### `output/scraped_data.csv`

Full record of every business found:

| Column | Description |
|--------|-------------|
| `name` | Business name |
| `niche` | Keyword used to find this business |
| `address` | Full address |
| `state` | State/region |
| `phone_number` | Phone number |
| `website` | Business website URL |
| `email` | Extracted email address |
| `result_url` | Google Maps listing URL |

### `emails.json`

The email tracking database. Each entry in `all_emails` looks like:
```json
"info@business.com": {
  "business_name": "Example Business",
  "added_date": "2026-03-31 09:15:22",
  "sent_date": "2026-03-31 11:30:00",
  "sent_count": 1
}
```

Emails are never sent twice — the manager checks `sent_count` before sending.

---

## Resetting Progress

### Reset scraper progress (start from the beginning of niches + locations)

```bash
python -c "import json; json.dump({'current_niche_index': 0, 'current_location_index': 0}, open('output/progress.json', 'w'), indent=2)"
```

### Clear the email database (delete all collected and sent records)

Delete `emails.json` — it will be recreated automatically on next run.

### Clear scraped businesses

Delete `output/scraped_data.csv` — it will be recreated automatically.

### Full reset (start completely fresh)

```bash
del emails.json
del output\scraped_data.csv
python -c "import json; json.dump({'current_niche_index': 0, 'current_location_index': 0}, open('output/progress.json', 'w'), indent=2)"
```

---

## Troubleshooting

### "No businesses found for this search"
Normal. Some keyword + location combinations return no results on Google Maps. The scraper logs this and moves on automatically.

### "Rate limit hit — waiting before next request"
Normal and expected. The rate limiter is protecting your IP from being blocked. No action needed.

### "Email extraction failed for website"
Normal. Not all businesses have a website, and not all websites list an email address publicly. The scraper tries up to 3 pages (home, contact, about) before moving on.

### "Authentication failed" when sending email
- Make sure you are using an **App Password**, not your real Gmail password
- Confirm 2-Factor Authentication is enabled on the Gmail account
- Re-generate a new App Password and update `email_config.json`

### "Daily sending limit exceeded"
- Gmail's daily sending limit was hit
- The email sender waits exactly 24 hours from the last successful email, then resumes automatically
- No action needed; it will recover on its own

### "No unsent emails available"
- The sender has caught up with the scraper
- The scraper is still running and will add more emails; the sender polls regularly
- Or all collected emails have already been sent; wait for the scraper to find more

### Browser window closes unexpectedly
- SeleniumBase UC Mode sometimes fails on first launch; the scraper retries automatically
- If it happens repeatedly, check that Google Chrome is up to date

### Bot crashes mid-run
Just re-run `python run_free_scraper.py`. Progress is saved to `output/progress.json` and `emails.json` after every record — you will not lose work.

---

## Safety and Limits

### Scraping limits (built-in, automatic)

| Limit | Value | Why |
|-------|-------|-----|
| Requests per minute | 10 | Avoids Google Maps IP bans |
| Requests per hour | 300 | Sustained safe rate |
| Requests per day | 5,000 | Daily safety cap |
| Random delay per request | 2–5 seconds | Mimics human browsing |

### Email sending limits (configurable in `bot_settings.json`)

| Setting | Recommended | Maximum safe |
|---------|-------------|-------------|
| `daily_email_limit` | 100–200 | 400 (Gmail hard limit) |
| `delay_between_emails` | 300–600 sec | 60 sec minimum |

### What NOT to do

- Do not set `delay_between_emails` below 60 seconds — Gmail may flag your account as a spammer
- Do not set `daily_email_limit` above 400 — Gmail will suspend sending for 24 hours
- Do not run multiple instances of the bot simultaneously — they will conflict on shared files
- Do not commit `email_config.json` or `.env` to a public repository — they contain your credentials

### Recommended `.gitignore` additions

```
email_config.json
.env
emails.json
output/
logs/
downloaded_files/
```
