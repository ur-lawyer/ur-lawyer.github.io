"""One-time script to authenticate with Google Search Console and save session"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config import GSC_PROPERTY_URL, GSC_CHROME_PROFILE_PATH


def first_time_login():
    """
    Interactive first-time login to Google Search Console
    This saves authentication session for future automated runs
    """
    print("=" * 60)
    print("🔐 Google Search Console - First Time Login")
    print("=" * 60)
    print(f"📁 Profile will be saved to: {GSC_CHROME_PROFILE_PATH}")
    print(f"🌐 Property: {GSC_PROPERTY_URL}")
    print()
    print("⚠️  INSTRUCTIONS:")
    print("   1. Chrome will open with Google Search Console")
    print("   2. Manually log in to your Google account")
    print("   3. Complete any 2FA/verification if required")
    print("   4. Wait until you see the GSC dashboard")
    print("   5. Press ENTER in this terminal to save session")
    print("=" * 60)
    
    input("Press ENTER to continue...")
    
    try:
        # Setup Chrome with user data directory
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={GSC_CHROME_PROFILE_PATH}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # Add flags to prevent crashes on macOS
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--no-sandbox")
        
        print("\n🚀 Launching Chrome browser...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navigate to Google Search Console
        gsc_url = f"https://search.google.com/search-console?resource_id={GSC_PROPERTY_URL}"
        print(f"🌐 Navigating to: {gsc_url}")
        driver.get(gsc_url)
        
        print("\n" + "=" * 60)
        print("✅ Chrome launched successfully!")
        print("=" * 60)
        print("👉 Please complete the following:")
        print("   1. Log in to your Google account")
        print("   2. Select your property if prompted")
        print("   3. Verify you can see the Search Console dashboard")
        print()
        print("⏸️  Once logged in, press ENTER here to save session...")
        print("=" * 60)
        
        input()
        
        print("\n🔍 Verifying authentication...")
        
        # Check if we're on Search Console page
        current_url = driver.current_url
        if "search.google.com/search-console" in current_url:
            print("✅ Authentication verified!")
            print(f"📝 Current URL: {current_url}")
            
            print("\n💾 Saving session...")
            print(f"📁 Profile saved at: {GSC_CHROME_PROFILE_PATH}")
            
            # Keep browser open for a moment to ensure cookies are saved
            time.sleep(2)
            
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Session saved successfully")
            print("=" * 60)
            print("📋 Next steps:")
            print("   1. You can now close this window")
            print("   2. Run gsc_automation.py to submit URLs automatically")
            print("   3. The saved session will be used for future runs")
            print("=" * 60)
            
        else:
            print("⚠️  Warning: You may not be logged in correctly")
            print(f"Current URL: {current_url}")
            print("Please verify manually before using automation")
        
        # Wait before closing
        input("\nPress ENTER to close browser...")
        driver.quit()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during login: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = first_time_login()
    
    if success:
        print("\n✅ Setup complete! You can now use gsc_automation.py")
    else:
        print("\n❌ Setup failed. Please try again or check the error messages.")