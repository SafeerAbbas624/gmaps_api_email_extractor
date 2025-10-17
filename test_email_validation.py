#!/usr/bin/env python
"""Test email validation"""

try:
    from email_scraper import EmailScraper
    print("Import successful")
    scraper = EmailScraper()
    print("EmailScraper instantiated")
    
    # Test emails
    test_emails = [
        ('info@lacasaditourist.comloginlogin', False),
        ('info@lacasaditourist.com', True),
        ('info@chiaiaviaggi.itindirizzolargo', False),
        ('info@chiaiaviaggi.it', True),
        ('081.5046756info@equadorviaggi.itnapoli', False),
        ('info@equadorviaggi.it', True),
        ('valid@example.com', True),
        ('test@domain.co.uk', True),
        ('conferme@atomikaviaggi.itindirizzovia', False),
        ('info@traveltips.itcontattaciil', False),
    ]
    
    print('\nEmail Validation Test:')
    print('=' * 70)
    passed = 0
    failed = 0
    for email, expected in test_emails:
        is_valid = scraper._is_valid_email(email)
        status = 'PASS' if is_valid == expected else 'FAIL'
        if is_valid == expected:
            passed += 1
        else:
            failed += 1
        print(f'{status:4} | {email:45} -> {is_valid} (expected {expected})')
    
    print('=' * 70)
    print(f'Results: {passed} passed, {failed} failed')
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

