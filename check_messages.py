#!/usr/bin/env python3
from email_messages import EMAIL_MESSAGES

print(f"Total messages: {len(EMAIL_MESSAGES)}")
print("\nMessage subjects:")
for i, msg in enumerate(EMAIL_MESSAGES, 1):
    print(f"{i}. {msg['subject']}")

