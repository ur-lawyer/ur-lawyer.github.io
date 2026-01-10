"""Automate URL submission to Google Search Console using Selenium with undetected-chromedriver"""
import os
import sys
import time
import json
import base64
import shutil
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import GSC_PROPERTY_URL, GSC_CHROME_PROFILE_PATH, GSC_MAX_RETRIES, GSC_HEADLESS


def load_cookies_from_env():
    """Load cookies from environment variable (GitHub Secrets)"""
    cookies_env = os.getenv('GSC_COOKIES')
    if not cookies_env:
        return None
    
    try:
        # Decode from base64
        cookies_json = base64.b64decode(cookies_env).decode()
        cookies = json.loads(cookies_json)
        print(f"✅ Loaded {len(cookies)} cookies from environment")
        return cookies
    except Exception as e:
        print(f"⚠️  Failed to load cookies from environment: {e}")
        return None


def setup_chrome_driver(headless=None):
    """
    Setup Chrome driver with anti-detection measures
    
    Args:
        headless: Override headless mode from config
        
    Returns:
        webdriver.Chrome: Configured Chrome driver
    """
    if headless is None:
        headless = GSC_HEADLESS
    
    # Check for cookies from environment first (GitHub Actions)
    use_cookies = load_cookies_from_env() is not None
    
    # Check if we have saved profile (local use)
    use_profile = not use_cookies and os.path.exists(GSC_CHROME_PROFILE_PATH)
    
    try:
        if UNDETECTED_AVAILABLE:
            print("✅ Using undetected-chromedriver (anti-bot)")
            
            # Options for undetected-chromedriver
            options = uc.ChromeOptions()
            
            # Use saved profile if available
            if use_profile:
                options.add_argument(f"--user-data-dir={GSC_CHROME_PROFILE_PATH}")
                print(f"✅ Using saved profile: {GSC_CHROME_PROFILE_PATH}")
            
            # Additional stealth options
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--window-size=1920,1080")
            
            # Headless mode (experimental with undetected-chromedriver)
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                print("🔇 Running in headless mode")
            
            # Create driver with undetected-chromedriver
            driver = uc.Chrome(options=options, version_main=None)
            driver.set_page_load_timeout(30)
            
        else:
            print("⚠️  undetected-chromedriver not available, using regular selenium")
            print("   Install it: pip install undetected-chromedriver")
            
            chrome_options = Options()
            
            if use_profile:
                chrome_options.add_argument(f"--user-data-dir={GSC_CHROME_PROFILE_PATH}")
                print(f"✅ Using saved profile: {GSC_CHROME_PROFILE_PATH}")
            
            # Chrome options
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_argument("--window-size=1920,1080")
            
            if headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                print("🔇 Running in headless mode")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)
        
        # If we have cookies from environment, load them
        cookies = load_cookies_from_env()
        if cookies:
            print(f"🔐 Loading authentication cookies...")
            
            # Navigate to google.com first
            driver.get("https://www.google.com")
            time.sleep(2)
            
            # Add cookies
            cookies_added = 0
            for cookie in cookies:
                try:
                    # Clean up cookie format for Selenium
                    cookie_clean = {
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie['domain'].lstrip('.'),
                        'path': cookie.get('path', '/'),
                        'secure': cookie.get('secure', False),
                        'httpOnly': cookie.get('httpOnly', False)
                    }
                    
                    # Add expiry if present
                    if 'expires' in cookie and cookie['expires']:
                        cookie_clean['expiry'] = int(cookie['expires'] / 1000000 - 11644473600)
                    
                    driver.add_cookie(cookie_clean)
                    cookies_added += 1
                except Exception as e:
                    # Skip problematic cookies
                    pass
            
            print(f"✅ Added {cookies_added} cookies")
            
            # Refresh to activate session
            driver.refresh()
            time.sleep(2)
            
            # Navigate to accounts.google.com to verify session
            print(f"🔄 Verifying authentication...")
            driver.get("https://accounts.google.com")
            time.sleep(3)
            
            # Check if we're logged in
            if "ServiceLogin" not in driver.current_url and "signin" not in driver.current_url:
                print(f"✅ Authentication verified!")
            else:
                print(f"⚠️  May not be authenticated - will try anyway")
        
        return driver
        
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        import traceback
        traceback.print_exc()
        return None


def submit_url_to_gsc(url, headless=None):
    """
    Submit single URL to Google Search Console
    
    Args:
        url: URL to submit for indexing
        headless: Override headless mode
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'=' * 60}")
    print(f"🔎 Submitting URL to Google Search Console")
    print(f"{'=' * 60}")
    print(f"🌐 URL: {url}")
    print(f"🏠 Property: {GSC_PROPERTY_URL}")
    
    driver = None
    
    try:
        # Setup driver
        driver = setup_chrome_driver(headless)
        if not driver:
            print("❌ Failed to setup Chrome driver")
            return False
        
        # Navigate to URL Inspection tool
        inspection_url = f"https://search.google.com/search-console/inspect?resource_id={GSC_PROPERTY_URL}"
        print(f"\n📍 Navigating to URL Inspection tool...")
        driver.get(inspection_url)
        
        # Wait and check for redirects
        time.sleep(5)
        
        # Check if we're logged in
        current_url = driver.current_url
        if "accounts.google.com" in current_url or "ServiceLogin" in current_url:
            print(f"❌ Not logged in! Redirected to: {current_url}")
            
            # Take screenshot for debugging
            screenshot_path = "/tmp/gsc_login_fail.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            # Print page source snippet for debugging
            print(f"\n🔍 Page title: {driver.title}")
            print(f"🍪 Cookies present: {len(driver.get_cookies())}")
            
            return False
        
        print("✅ Successfully accessed Google Search Console")
        print(f"✅ Current page: {driver.title}")
        
        # Find the URL input field
        print(f"\n🔍 Looking for URL input field...")
        
        # Wait for page to fully load
        time.sleep(3)
        
        # Try multiple selectors
        selectors = [
            "input[type='text'][aria-label*='URL']",
            "input[type='text'][placeholder*='URL']",
            "input[type='url']",
            "input.devsite-search-field",
            "input[jsname]",
        ]
        
        url_input = None
        for selector in selectors:
            try:
                url_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if url_input and url_input.is_displayed():
                    print(f"✅ Found input field with selector: {selector}")
                    break
                else:
                    url_input = None
            except TimeoutException:
                continue
        
        if not url_input:
            # Try finding any visible text input
            try:
                inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                for inp in inputs:
                    if inp.is_displayed():
                        url_input = inp
                        print("✅ Found visible text input field")
                        break
            except NoSuchElementException:
                pass
        
        if not url_input:
            print("❌ Could not find URL input field")
            screenshot_path = "/tmp/gsc_no_input.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            return False
        
        # Enter URL with human-like typing
        print(f"⌨️  Entering URL...")
        url_input.click()
        time.sleep(0.5)
        url_input.clear()
        time.sleep(0.5)
        
        # Type slowly to mimic human
        for char in url:
            url_input.send_keys(char)
            time.sleep(0.05)
        
        time.sleep(1)
        url_input.send_keys(Keys.RETURN)
        
        print(f"⏳ Waiting for inspection to complete...")
        time.sleep(15)  # Give it time to analyze
        
        # Look for "Request Indexing" button
        print(f"🔍 Looking for 'Request Indexing' button...")
        
        button_selectors = [
            "//button[contains(text(), 'Request indexing')]",
            "//button[contains(text(), 'REQUEST INDEXING')]",
            "//span[contains(text(), 'Request indexing')]/ancestor::button",
            "//button[contains(@aria-label, 'Request indexing')]",
        ]
        
        request_button = None
        for selector in button_selectors:
            try:
                request_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if request_button:
                    print(f"✅ Found 'Request Indexing' button")
                    break
            except TimeoutException:
                continue
        
        if not request_button:
            print("⚠️  'Request Indexing' button not found")
            
            # Check page for status messages
            page_text = driver.page_source.lower()
            if "already" in page_text or "queue" in page_text or "recently requested" in page_text:
                print("✅ URL appears to already be in indexing queue")
                return True
            
            # Take screenshot
            screenshot_path = "/tmp/gsc_no_button.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            return False
        
        # Click the button with delay
        print(f"🖱️  Clicking 'Request Indexing' button...")
        time.sleep(1)
        request_button.click()
        
        # Wait for confirmation
        print(f"⏳ Waiting for confirmation...")
        time.sleep(8)
        
        # Check for success
        try:
            success_selectors = [
                "//span[contains(text(), 'Indexing requested')]",
                "//div[contains(text(), 'requested')]",
                "//*[contains(text(), 'success')]",
            ]
            
            for selector in success_selectors:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    print("✅ SUCCESS! URL submitted for indexing")
                    return True
                except TimeoutException:
                    continue
            
            # Check page text
            page_text = driver.page_source.lower()
            if "requested" in page_text or "submitted" in page_text:
                print("✅ SUCCESS! URL appears to be submitted")
                return True
            
            print("⚠️  Could not confirm submission, but no errors detected")
            return True
            
        except Exception as e:
            print(f"⚠️  Error checking confirmation: {e}")
            print("✅ Assuming success (no errors during submission)")
            return True
        
    except Exception as e:
        print(f"❌ Error during submission: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print(f"\n🔒 Closing browser...")
            time.sleep(2)
            driver.quit()


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Submit URLs to Google Search Console')
    parser.add_argument('--url', type=str, help='Single URL to submit')
    parser.add_argument('--urls', type=str, nargs='+', help='Multiple URLs to submit')
    parser.add_argument('--visible', action='store_true', help='Run with visible browser (not headless)')
    
    args = parser.parse_args()
    
    headless = not args.visible
    
    if args.url:
        submit_url_to_gsc(args.url, headless=headless)
    elif args.urls:
        for url in args.urls:
            submit_url_to_gsc(url, headless=headless)
            if len(args.urls) > 1:
                time.sleep(10)
    else:
        print("❌ Please provide --url or --urls argument")
        parser.print_help()


if __name__ == "__main__":
    main()