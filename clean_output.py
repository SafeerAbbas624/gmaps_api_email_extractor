#!/usr/bin/env python
"""Clean output file by removing rows with NOT AVAILABLE emails"""

import pandas as pd
import os
from datetime import datetime

try:
    output_file = 'output/scraped_data.csv'
    
    if not os.path.exists(output_file):
        print("❌ Output file not found!")
        exit(1)
    
    # Read the output file
    df = pd.read_csv(output_file)
    
    print('📊 CLEANING OUTPUT FILE:')
    print('=' * 100)
    print(f'Total records before cleaning: {len(df)}')
    
    # Count records with and without emails
    with_email = df[df['email'] != 'NOT AVAILABLE']
    without_email = df[df['email'] == 'NOT AVAILABLE']
    
    print(f'Records with emails: {len(with_email)}')
    print(f'Records without emails (to be removed): {len(without_email)}')
    print()
    
    # Remove rows with NOT AVAILABLE emails
    df_cleaned = df[df['email'] != 'NOT AVAILABLE'].copy()
    
    # Reset index
    df_cleaned.reset_index(drop=True, inplace=True)
    
    # Save the cleaned data
    df_cleaned.to_csv(output_file, index=False)
    
    print(f'✅ Cleaned output saved!')
    print(f'Total records after cleaning: {len(df_cleaned)}')
    print()
    
    # Display sample of cleaned data
    print('Sample of cleaned data:')
    print('-' * 100)
    for idx, (i, row) in enumerate(df_cleaned.head(10).iterrows()):
        print(f'{idx+1:2}. {row["name"]:30} | {row["email"]:35} | {row["phone_number"]}')
    
    print()
    print('=' * 100)
    print(f'✅ File saved: {output_file}')
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

