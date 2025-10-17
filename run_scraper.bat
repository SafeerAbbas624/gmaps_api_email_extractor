@echo off
echo ===============================================================================
echo                        GOOGLE MAPS SCRAPER - MAIN MENU
echo ===============================================================================
echo.
echo 📚 FIRST TIME? READ THESE FILES:
echo    📄 API_SETUP_INSTRUCTIONS.txt  - How to get Google Maps API key
echo    📄 HOW_TO_RUN_SCRAPER.txt      - Step-by-step running guide
echo.
echo 🎯 WHAT WOULD YOU LIKE TO DO?
echo.
echo 1. 🎮 Run demo (no API key needed - see how it works)
echo 2. 🧪 Test single search (requires API key)
echo 3. 🚀 Start continuous scraping (requires API key)
echo 4. 📊 View progress and statistics
echo 5. 🧹 Clean data (remove duplicates)
echo 6. 📖 Open instruction files
echo 7. ❌ Exit

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo.
    echo 🎮 Running demo (no API key needed)...
    echo This shows how the scraper works with sample data.
    echo.
    python demo.py
    echo.
    pause
) else if "%choice%"=="2" (
    echo.
    echo 🧪 Testing single search...
    set /p niche="Enter niche (e.g., roofers): "
    set /p location="Enter location (e.g., San Diego, CA): "
    echo.
    echo Testing: %niche% in %location%
    echo This will take 10-30 seconds...
    python main.py --mode single --niche "%niche%" --location "%location%"
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Starting continuous scraping...
    echo This will process ALL niches and locations in your input files.
    echo Press Ctrl+C to stop gracefully (progress will be saved).
    echo.
    pause
    python main.py --mode continuous
    echo.
    pause
) else if "%choice%"=="4" (
    echo.
    echo 📊 Current progress:
    python utils.py progress
    echo.
    echo 📈 Data statistics:
    python utils.py stats
    echo.
    pause
) else if "%choice%"=="5" (
    echo.
    echo 🧹 Cleaning data (removing duplicates)...
    python main.py --mode cleanup
    echo.
    pause
) else if "%choice%"=="6" (
    echo.
    echo 📖 Opening instruction files...
    echo.
    echo Opening API setup instructions...
    start notepad API_SETUP_INSTRUCTIONS.txt
    echo Opening running instructions...
    start notepad HOW_TO_RUN_SCRAPER.txt
    echo.
    echo Files opened in Notepad. Read them for detailed instructions.
    pause
) else if "%choice%"=="7" (
    echo.
    echo ❌ Goodbye! Happy scraping!
) else (
    echo.
    echo ❌ Invalid choice. Please run again and choose 1-7.
    pause
)
