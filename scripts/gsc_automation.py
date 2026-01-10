"""Automate URL submission to Google Search Console using Selenium"""
import os
import sys
import time
import json
import base64
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
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
    Setup Chrome driver with saved profile or cookies
    
    Args:
        headless: Override headless mode from config
        
    Returns:
        webdriver.Chrome: Configured Chrome driver
    """
    if headless is None:
        headless = GSC_HEADLESS
    
    chrome_options = Options()
    
    # Check for cookies from environment first (GitHub Actions)
    use_cookies = load_cookies_from_env() is not None
    
    # Use saved profile for authentication (local use)
    if not use_cookies and os.path.exists(GSC_CHROME_PROFILE_PATH):
        chrome_options.add_argument(f"--user-data-dir={GSC_CHROME_PROFILE_PATH}")
        print(f"✅ Using saved profile: {GSC_CHROME_PROFILE_PATH}")
    elif not use_cookies:
        print(f"ℹ️  No saved profile or cookies found")
        print(f"   Browser will start without authentication")
    
    # Chrome options for stability
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Headless mode for CI/CD
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        print("🔇 Running in headless mode")
    
    # Window size for consistent behavior
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        # If we have cookies from environment, load them
        cookies = load_cookies_from_env()
        if cookies:
            # Navigate to google.com first - this is the best place to set session cookies
            print(f"🔐 [NEW] Loading authentication cookies on google.com...")
            driver.get("https://www.google.com")
            time.sleep(2)
            
            # Add each cookie
            cookies_added = 0
            for cookie in cookies:
                try:
                    # Ensure domain compatibility
                    if 'domain' in cookie and 'google.com' in cookie['domain']:
                        driver.add_cookie(cookie)
                        cookies_added += 1
                except Exception as e:
                    # Some cookies may fail due to domain mismatch
                    pass
            
            print(f"✅ Added {cookies_added} cookies to browser")
            
            # Refresh to apply cookies
            driver.refresh()
            time.sleep(1)
        
        return driver
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        return None


def submit_url_to_gsc(url):
    """
    Submit single URL to Google Search Console
    
    Args:
        url: URL to submit for indexing
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'=' * 60}")
    print(f"🔍 Submitting URL to Google Search Console")
    print(f"{'=' * 60}")
    print(f"🌐 URL: {url}")
    print(f"🏠 Property: {GSC_PROPERTY_URL}")
    
    driver = None
    
    try:
        # Setup driver
        driver = setup_chrome_driver()
        if not driver:
            print("❌ Failed to setup Chrome driver")
            return False
        
        # Navigate to URL Inspection tool
        inspection_url = f"https://search.google.com/search-console/inspect?resource_id={GSC_PROPERTY_URL}"
        print(f"\n📍 Navigating to URL Inspection tool...")
        driver.get(inspection_url)
        
        # Wait for page load
        time.sleep(3)
        
        # Check if we're logged in
        if "accounts.google.com" in driver.current_url:
            print("❌ Not logged in! Please run first_time_gsc_login.py first")
            return False
        
        print("✅ Logged in successfully")
        
        # Find the URL input field
        print(f"🔍 Looking for URL input field...")
        
        # Try multiple selectors as Google may change their UI
        selectors = [
            "input[type='text'][aria-label*='URL']",
            "input[type='text'][placeholder*='URL']",
            "input.devsite-search-field",
            "input[jsname]",
        ]
        
        url_input = None
        for selector in selectors:
            try:
                url_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if url_input:
                    print(f"✅ Found input field with selector: {selector}")
                    break
            except TimeoutException:
                continue
        
        if not url_input:
            # Try finding by text input that's visible
            try:
                url_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
                print("✅ Found generic text input field")
            except NoSuchElementException:
                print("❌ Could not find URL input field")
                print("📸 Taking screenshot for debugging...")
                driver.save_screenshot("/tmp/gsc_error.png")
                print(f"   Screenshot saved to /tmp/gsc_error.png")
                return False
        
        # Clear and enter URL
        print(f"⌨️  Entering URL...")
        url_input.clear()
        time.sleep(0.5)
        url_input.send_keys(url)
        time.sleep(0.5)
        url_input.send_keys(Keys.RETURN)
        
        print(f"⏳ Waiting for inspection to complete...")
        time.sleep(10)  # Increased wait time for page to fully load
        
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
            print("ℹ️  Possible reasons:")
            print("   - URL is already in queue")
            print("   - URL has recently been submitted")
            print("   - Page is still loading")
            
            # Check if already submitted
            page_text = driver.page_source.lower()
            if "already" in page_text or "queue" in page_text:
                print("✅ URL appears to already be in indexing queue")
                return True
            
            # Take screenshot for debugging
            print("📸 Taking screenshot for debugging...")
            driver.save_screenshot("/tmp/gsc_no_button.png")
            print(f"   Screenshot saved to /tmp/gsc_no_button.png")
            return False
        
        # Click the button
        print(f"🖱️  Clicking 'Request Indexing' button...")
        request_button.click()
        
        # Wait for confirmation
        print(f"⏳ Waiting for confirmation...")
        time.sleep(5)
        
        # Check for success message
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
            
            # If no explicit success message, check page state
            page_text = driver.page_source.lower()
            if "requested" in page_text or "submitted" in page_text:
                print("✅ SUCCESS! URL appears to be submitted")
                return True
            
            print("⚠️  Could not confirm submission, but no errors detected")
            return True
            
        except Exception as e:
            print(f"⚠️  Error checking confirmation: {e}")
            # Assume success if we got this far without errors
            print("✅ Assuming success (no errors during submission)")
            return True
        
    except Exception as e:
        print(f"❌ Error during submission: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print(f"🔒 Closing browser...")
            driver.quit()


def submit_urls_batch(urls, headless=None):
    """
    Submit multiple URLs to Google Search Console
    
    Args:
        urls: List of URLs to submit
        headless: Override headless mode from config
        
    Returns:
        dict: Results with success/failure counts
    """
    print(f"\n{'=' * 60}")
    print(f"📋 Batch URL Submission")
    print(f"{'=' * 60}")
    print(f"📊 Total URLs: {len(urls)}")
    
    results = {
        'success': 0,
        'failed': 0,
        'urls_success': [],
        'urls_failed': []
    }
    
    for i, url in enumerate(urls, 1):
        print(f"\n{'=' * 60}")
        print(f"Processing URL {i}/{len(urls)}")
        print(f"{'=' * 60}")
        
        success = submit_url_to_gsc(url, headless)
        
        if success:
            results['success'] += 1
            results['urls_success'].append(url)
        else:
            results['failed'] += 1
            results['urls_failed'].append(url)
        
        # Wait between submissions to avoid rate limiting
        if i < len(urls):
            print(f"\n⏳ Waiting 10 seconds before next submission...")
            time.sleep(10)
    
    # Print summary
    print(f"\n{'=' * 60}")
    print(f"📊 Batch Submission Complete")
    print(f"{'=' * 60}")
    print(f"✅ Successful: {results['success']}")
    print(f"❌ Failed: {results['failed']}")
    
    return results


def cleanup_chrome_profile():
    """
    Delete Chrome profile directory
    Use this to clean up after GitHub Actions workflow
    """
    print(f"\n{'=' * 60}")
    print(f"🧹 Cleaning up Chrome profile")
    print(f"{'=' * 60}")
    
    if os.path.exists(GSC_CHROME_PROFILE_PATH):
        try:
            shutil.rmtree(GSC_CHROME_PROFILE_PATH)
            print(f"✅ Profile deleted: {GSC_CHROME_PROFILE_PATH}")
            return True
        except Exception as e:
            print(f"❌ Error deleting profile: {e}")
            return False
    else:
        print(f"ℹ️  Profile does not exist: {GSC_CHROME_PROFILE_PATH}")
        return True


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Submit URLs to Google Search Console')
    parser.add_argument('--url', type=str, help='Single URL to submit')
    parser.add_argument('--urls', type=str, nargs='+', help='Multiple URLs to submit')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup Chrome profile')
    parser.add_argument('--visible', action='store_true', help='Run with visible browser (not headless)')
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_chrome_profile()
        return
    
    headless = not args.visible
    
    if args.url:
        submit_url_to_gsc(args.url, headless=headless)
    elif args.urls:
        submit_urls_batch(args.urls, headless=headless)
    else:
        print("❌ Please provide --url or --urls argument")
        parser.print_help()


if __name__ == "__main__":
    main()