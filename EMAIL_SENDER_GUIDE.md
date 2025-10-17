# 📧 GMAPS Email Sender - Complete Guide

## Overview

The **GMAPS Email Sender** is a powerful automated email sending tool designed to work seamlessly with the Google Maps Email Scraper. It sends emails to scraped email addresses with a daily limit of 500 emails and automatic reset at midnight.

---

## ✨ Features

✅ **Daily Email Limit**
- Send up to 500 emails per day
- Automatic reset at midnight
- Resume from where you left off

✅ **Smart Tracking**
- JSON-based email tracking
- Prevents duplicate sends
- Tracks success/failure status
- Maintains sending history

✅ **Professional Email Sending**
- Gmail SMTP integration
- Secure SSL connection
- UTF-8 encoding support
- Professional formatting

✅ **Beautiful UI**
- Amazing ASCII art banner
- Real-time progress display
- Status updates every 10 emails
- Color-coded messages

✅ **Robust Error Handling**
- Automatic retry logic
- Detailed logging
- Error recovery
- Graceful shutdown

✅ **Parallel Execution**
- Run alongside scraper
- Independent threads
- Synchronized operations
- Real-time coordination

---

## 🚀 Quick Start

### Option 1: Run Email Sender Alone

```bash
python email_sender.py
```

### Option 2: Run Scraper + Email Sender in Parallel

```bash
python run_scraper_and_sender.py
```

---

## 📋 Configuration

### Step 1: Prepare Your Gmail Account

1. **Enable 2-Factor Authentication** (if not already enabled)
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

### Step 2: Run the Email Sender

```bash
python email_sender.py
```

### Step 3: Enter Configuration

When prompted, enter:

```
📧 Enter your Gmail address: your_email@gmail.com
🔐 Enter your Gmail App Password: xxxx xxxx xxxx xxxx
📝 Enter the message to send: (Your message here)
```

---

## 📊 How It Works

### Daily Limit System

```
Day 1:
├─ Send 500 emails
├─ Reach daily limit
└─ Wait for midnight

Day 2 (After Midnight):
├─ Reset counter to 0
├─ Continue from email #501
└─ Send next 500 emails
```

### Email Tracking

The system maintains `email_sent_tracking.json`:

```json
{
  "last_date": "2025-10-17",
  "sent_today": 250,
  "total_sent": 750,
  "failed_count": 5,
  "sent_emails": [
    {
      "email": "user@example.com",
      "timestamp": "2025-10-17T10:30:45.123456",
      "status": "success"
    }
  ]
}
```

### Data Flow

```
Google Maps Scraper
        ↓
output/scraped_data.csv
        ↓
Email Sender
        ↓
Gmail SMTP Server
        ↓
Recipients
```

---

## 🎯 Usage Examples

### Example 1: Send Marketing Emails

```
📧 Enter your Gmail address: marketing@company.com
🔐 Enter your Gmail App Password: xxxx xxxx xxxx xxxx
📝 Enter the message to send:

Dear Business Owner,

We have a special offer for you!
Check our website for more details.

Best regards,
Marketing Team
```

### Example 2: Send Notifications

```
📧 Enter your Gmail address: notifications@company.com
🔐 Enter your Gmail App Password: xxxx xxxx xxxx xxxx
📝 Enter the message to send:

Hello,

This is an important notification about your business listing.
Please review the attached information.

Thank you
```

---

## 📈 Status Display

The sender displays real-time status:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                          📊 SENDING STATUS 📊                             ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  Today's Progress:     250/500 emails sent (50.0%)                        ║
║  Remaining Today:      250 emails                                         ║
║  Total Sent (All):     750 emails                                         ║
║  Failed Attempts:      5 emails                                           ║
║  Last Updated:         2025-10-17 14:30:45                                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## 🔧 Advanced Configuration

### Modify Daily Limit

Edit `email_sender.py`:

```python
self.daily_limit = 500  # Change to desired limit
```

### Change Email Provider

For non-Gmail providers, modify the SMTP settings:

```python
# For Outlook
server = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

# For Yahoo
server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
```

### Adjust Delay Between Emails

Edit `email_sender.py`:

```python
time.sleep(1)  # Change to desired delay in seconds
```

---

## 📝 Logging

All activities are logged to `email_sender.log`:

```
2025-10-17 10:30:45,123 - EmailSender - INFO - Email sent successfully to user@example.com
2025-10-17 10:30:46,456 - EmailSender - INFO - Tracking data saved
2025-10-17 10:30:47,789 - EmailSender - INFO - Loaded tracking data: 250 sent today, 750 total
```

---

## ⚠️ Important Notes

### Gmail App Passwords

- **Do NOT use your regular Gmail password**
- Use the 16-character App Password generated in Google Account settings
- App Passwords only work with 2-Factor Authentication enabled

### Daily Limits

- Gmail allows ~500 emails per day from a single account
- The script enforces this limit automatically
- Exceeding limits may result in account suspension

### Email Content

- Keep messages professional and relevant
- Avoid spam-like content
- Include unsubscribe information if required by law
- Comply with CAN-SPAM Act (if in USA)

### CSV File Format

The scraper must create `output/scraped_data.csv` with columns:
- `name` - Business name
- `email` - Email address
- `phone_number` - Phone number
- Other fields...

---

## 🐛 Troubleshooting

### Issue: "Authentication failed"

**Solution:**
- Verify Gmail address is correct
- Ensure you're using App Password, not regular password
- Check 2-Factor Authentication is enabled

### Issue: "CSV file not found"

**Solution:**
- Run the scraper first to generate `output/scraped_data.csv`
- Verify the file path is correct
- Check file permissions

### Issue: "No emails found to send"

**Solution:**
- Ensure scraper has completed and found emails
- Check CSV file contains valid email addresses
- Verify emails are not marked as "NOT AVAILABLE"

### Issue: "Daily limit reached"

**Solution:**
- This is normal behavior
- The script will wait until midnight
- Resume automatically the next day

---

## 📞 Support

For issues or questions:

**Developer:** Safeer Abbas
- **Email:** safeerabbas.624@gmail.com
- **WhatsApp:** +923312378492

---

## 📄 License

This tool is provided as-is for personal and business use.

---

## 🎉 Summary

The GMAPS Email Sender provides:
- ✅ Automated email sending
- ✅ Daily limit enforcement
- ✅ Professional tracking
- ✅ Beautiful UI
- ✅ Robust error handling
- ✅ Parallel execution capability

**Ready to send emails at scale!** 🚀

