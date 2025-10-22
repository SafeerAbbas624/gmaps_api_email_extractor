"""
Setup script for Google Maps Scraper
Run this to set up the environment and test the installation
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment file"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("Creating .env file from template...")
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
            print("⚠️  Please edit .env and add your Google Maps API key")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['input', 'output', 'logs', 'backups']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_api_key():
    """Check if API key is configured"""
    load_dotenv()
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Google Maps API key not configured")
        print("Please edit .env file and add your API key")
        return False
    else:
        print("✅ Google Maps API key found")
        return True

def run_tests():
    """Run the test suite"""
    print("\nRunning tests...")
    try:
        subprocess.check_call([sys.executable, "test_scraper.py"])
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Some tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("Google Maps Scraper Setup")
    print("=" * 30)
    
    success = True
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Setup environment
    if not setup_environment():
        success = False
    
    # Create directories
    create_directories()
    
    # Check API key
    api_key_ok = check_api_key()
    
    if api_key_ok:
        # Run tests
        if not run_tests():
            success = False
    else:
        print("⚠️  Skipping tests due to missing API key")
    
    print("\n" + "=" * 30)
    if success and api_key_ok:
        print("✅ Setup completed successfully!")
        print("\nYou can now run the scraper:")
        print("  python main.py --mode single --niche 'roofers' --location 'San Diego, CA'")
        print("  python main.py --mode continuous")
    elif success:
        print("⚠️  Setup completed but API key needs configuration")
        print("Please edit .env file and add your Google Maps API key")
    else:
        print("❌ Setup failed. Please check the errors above")

if __name__ == "__main__":
    main()
