#!/usr/bin/env python3
"""
Test script for dual API system
Tests API initialization, usage tracking, and switching
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_manager import APIManager
from config import config

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def test_api_initialization():
    """Test API initialization"""
    print_header("TEST 1: API INITIALIZATION")
    
    try:
        api_manager = APIManager()
        print("✅ APIManager initialized successfully")
        print(f"   API 1 Key: {config.google_maps_api_key[:20]}...")
        print(f"   API 2 Key: {config.google_maps_api_key_2[:20]}...")
        print(f"   Current API: {api_manager.current_api}")
        return api_manager
    except Exception as e:
        print(f"❌ Failed to initialize APIManager: {e}")
        return None

def test_usage_tracking(api_manager):
    """Test usage tracking"""
    print_header("TEST 2: USAGE TRACKING")
    
    try:
        # Record some requests
        print("Recording 10 requests on API 1...")
        for i in range(10):
            api_manager.record_request()
        
        # Record some emails
        print("Recording 5 emails found...")
        for i in range(5):
            api_manager.record_email_found()
        
        # Check status
        status = api_manager.get_status()
        print(status)
        
        # Check usage data
        usage = api_manager.usage_data
        print(f"\n✅ Usage Data:")
        print(f"   API 1 Daily Requests: {usage['api_1']['daily_requests']}")
        print(f"   API 1 Monthly Requests: {usage['api_1']['monthly_requests']}")
        print(f"   API 2 Daily Requests: {usage['api_2']['daily_requests']}")
        print(f"   API 2 Monthly Requests: {usage['api_2']['monthly_requests']}")
        print(f"   Daily Emails: {usage['daily_emails']}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to track usage: {e}")
        return False

def test_daily_email_limit(api_manager):
    """Test daily email limit"""
    print_header("TEST 3: DAILY EMAIL LIMIT (500)")
    
    try:
        # Reset to test
        api_manager.usage_data['daily_emails'] = 495
        api_manager._save_usage_data()
        
        print("Current daily emails: 495")
        print("Recording 5 more emails...")
        
        for i in range(5):
            api_manager.record_email_found()
            print(f"  Email {i+1}: {api_manager.usage_data['daily_emails']}/500")
        
        # Check if limit is reached
        if api_manager.check_daily_email_limit():
            print("✅ Daily email limit correctly detected at 500 emails")
            return True
        else:
            print("❌ Daily email limit not detected")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test daily email limit: {e}")
        return False

def test_monthly_limit(api_manager):
    """Test monthly request limit"""
    print_header("TEST 4: MONTHLY REQUEST LIMIT (11K)")
    
    try:
        # Reset to test
        api_manager.usage_data['api_1']['monthly_requests'] = 10990
        api_manager._save_usage_data()
        
        print("API 1 monthly requests: 10990")
        print("Recording 10 requests...")
        
        for i in range(10):
            api_manager.record_request()
            print(f"  Request {i+1}: {api_manager.usage_data['api_1']['monthly_requests']}/11000")
        
        # Check if limit is reached
        api1_limit, api2_limit = api_manager.check_monthly_limit()
        if api1_limit:
            print("✅ API 1 monthly limit correctly detected at 11000 requests")
            return True
        else:
            print("❌ API 1 monthly limit not detected")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test monthly limit: {e}")
        return False

def test_api_switching(api_manager):
    """Test API switching"""
    print_header("TEST 5: API SWITCHING")
    
    try:
        # Reset
        api_manager.usage_data['api_1']['monthly_requests'] = 11000
        api_manager.usage_data['api_2']['monthly_requests'] = 5000
        api_manager.current_api = 1
        api_manager._save_usage_data()
        
        print(f"Current API: {api_manager.current_api}")
        print("API 1 monthly requests: 11000 (at limit)")
        print("API 2 monthly requests: 5000 (available)")
        
        # Try to switch
        if api_manager.switch_api():
            print(f"✅ Successfully switched to API {api_manager.current_api}")
            return True
        else:
            print("❌ Failed to switch API")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test API switching: {e}")
        return False

def test_usage_persistence(api_manager):
    """Test usage data persistence"""
    print_header("TEST 6: USAGE DATA PERSISTENCE")
    
    try:
        # Save current usage
        api_manager._save_usage_data()
        print("✅ Usage data saved to file")
        
        # Load it back
        loaded_data = api_manager._load_usage_data()
        print("✅ Usage data loaded from file")
        
        # Verify
        if loaded_data['daily_emails'] == api_manager.usage_data['daily_emails']:
            print("✅ Usage data correctly persisted and loaded")
            return True
        else:
            print("❌ Usage data mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test persistence: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  DUAL API SYSTEM TEST SUITE".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    results = {}
    
    # Test 1: Initialization
    api_manager = test_api_initialization()
    results['Initialization'] = api_manager is not None
    
    if not api_manager:
        print("\n❌ Cannot continue without API manager")
        return
    
    # Test 2: Usage Tracking
    results['Usage Tracking'] = test_usage_tracking(api_manager)
    
    # Test 3: Daily Email Limit
    results['Daily Email Limit'] = test_daily_email_limit(api_manager)
    
    # Test 4: Monthly Request Limit
    results['Monthly Request Limit'] = test_monthly_limit(api_manager)
    
    # Test 5: API Switching
    results['API Switching'] = test_api_switching(api_manager)
    
    # Test 6: Usage Persistence
    results['Usage Persistence'] = test_usage_persistence(api_manager)
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Dual API system is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    print("\n" + "█"*70 + "\n")

if __name__ == "__main__":
    main()

