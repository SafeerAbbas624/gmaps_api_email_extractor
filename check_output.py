#!/usr/bin/env python
"""Check the output file for emails"""

import pandas as pd
import os

try:
    # Check if file exists
    if not os.path.exists('output/scraped_data.csv'):
        print("❌ Output file not found!")
        exit(1)
    
    # Read the output file
    df = pd.read_csv('output/scraped_data.csv')
    
    print('📊 SCRAPED DATA WITH EMAILS:')
    print('=' * 100)
    print(f'Total records: {len(df)}')
    print()
    
    # Show records with emails
    emails_found = df[df['email'] != 'NOT AVAILABLE']
    print(f'Records with emails: {len(emails_found)}')
    print()
    
    # Display first 15 records with emails
    print('Sample of scraped data with emails:')
    print('-' * 100)
    for idx, (i, row) in enumerate(emails_found.head(15).iterrows()):
        print(f'{idx+1:2}. {row["name"]:30} | {row["email"]:35} | {row["phone_number"]}')
        
    print()
    print('=' * 100)
    
    # Check for any malformed emails
    print('\nChecking for malformed emails...')
    malformed = []
    for idx, row in df.iterrows():
        email = row['email']
        if email != 'NOT AVAILABLE':
            # Check for common malformation patterns
            if any(word in email.lower() for word in ['login', 'indirizzo', 'napoli', 'roma', 'milano', 'via', 'corso', 'piazza', 'viale', 'contattaci']):
                malformed.append((row['name'], email))
    
    if malformed:
        print(f'⚠️  Found {len(malformed)} potentially malformed emails:')
        for name, email in malformed[:5]:
            print(f'   - {name}: {email}')
    else:
        print('✅ No malformed emails detected!')
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

