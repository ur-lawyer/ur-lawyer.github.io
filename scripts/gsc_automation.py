"""
GSC Automation Library
Contains the core logic for controlling Chrome and interacting with Google Search Console.
"""
import os
import time
import shutil
import base64
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class GSCAutomation:
    def __init__(self, profile_path=None, headless=False, record_video=False):
        """
        Initialize GSC Automation Bot
        
        Args:
            profile_path (str): Path to Chrome profile directory
            headless (bool): Run in headless mode
            record_video (bool): Enable video recording (not implemented directly in Selenium, used by caller)
        """
        self.profile_path = profile_path
        self.headless = headless
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome Driver"""
        chrome_options = Options()
        
        if self.profile_path:
            # Create directory if not exists
            if not os.path.exists(self.profile_path):
                os.makedirs(self.profile_path, exist_ok=True)
            chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
            print(f"✅ Using Chrome profile: {self.profile_path}")
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # Anti-detection
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            
            # Navigate to google.com to ensure session validity
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            # Check login status
            if self.is_logged_in():
                 print("✅ Valid session detected")
            else:
                 print("ℹ️  Not logged in - Manual login may be required")
                 
        except Exception as e:
            print(f"❌ Error setting up driver: {e}")
            raise

    def is_logged_in(self):
        """Check if logged into Google"""
        try:
            # If 'Sign in' button exists or accounts.google.com in url
            if "accounts.google.com" in self.driver.current_url:
                return False
            
            # Look for profile image or similar logged-in indicators
            # This is a loose check; improved by context
            return True
        except:
            return False

    def get_property_id(self, domain_url, use_domain_property=False):
        """
        Get the GSC property ID (sc-resource-id) for a domain
        For now, returns the URL itself as that works for URL-prefix properties
        """
        # For domain properties, it might need 'sc-domain:example.com'
        if use_domain_property:
            domain = domain_url.replace("https://", "").replace("http://", "").strip("/")
            return f"sc-domain:{domain}"
        return domain_url

    def submit_url(self, url, property_id):
        """
        Submit a URL to GSC
        Returns:
            True: Success
            'already_requested': Already in queue
            'quota_reached': Daily limit hit
            False: Failed
        """
        if not self.driver:
            return False
            
        try:
            # 1. Navigate to URL Inspection
            import urllib.parse
            encoded_resource = urllib.parse.quote(property_id)
            inspection_url = f"https://search.google.com/search-console/inspect?resource_id={encoded_resource}"
            
            print(f"📍 Navigating to Inspection Tool...")
            self.driver.get(inspection_url)
            time.sleep(5)
            
            # Check fail redirect
            if "accounts.google.com" in self.driver.current_url:
                print("❌ Redirected to login - session invalid")
                return False

            # 2. Enter URL
            print(f"⌨️  Inspecting URL: {url}")
            
            # Try to find input
            try:
                # Selector strategy
                selectors = [
                    "input[aria-label='Inspect any URL in the current property']",
                    "input[jsname='UD358d']",  # Common obfuscated name
                    "input[type='text']"       # Fallback
                ]
                
                inp = None
                for sel in selectors:
                    try:
                        inp = self.driver.find_element(By.CSS_SELECTOR, sel)
                        if inp.is_displayed():
                            break
                    except:
                        continue
                
                if not inp:
                    print("❌ Could not find search bar")
                    return False
                
                # Clear and type
                # Sometimes simply clicking and typing works best
                inp.click()
                time.sleep(0.5)
                # clear via keys if clear() is flaky
                inp.send_keys(Keys.COMMAND + "a")
                inp.send_keys(Keys.DELETE)
                
                inp.send_keys(url)
                time.sleep(0.5)
                inp.send_keys(Keys.RETURN)
                
            except Exception as e:
                print(f"❌ Error entering URL: {e}")
                return False

            # 3. Wait for retrieval
            print("⏳ Retrieving data from Google Index...")
            time.sleep(15) # Wait for initial processing

            # 4. Look for "Request Indexing"
            try:
                # Check for "Request Indexing" button
                # Be careful not to click "Test Live URL" unless necessary
                # "Request Indexing" is usually consistent
                btn = WebDriverWait(self.driver, 10).until(
                   EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Request indexing')]"))
                )
                print("✅ Found 'Request Indexing' button")
                btn.click()
                
            except TimeoutException:
                # Check if it says "Indexing requested" (Already done)
                src = self.driver.page_source
                if "Indexing requested" in src:
                    return 'already_requested'
                
                print("⚠️  Button not found or not clickable")
                return False
            
            # 5. Handle Popup/Confirmation
            print("⏳ Handling submission popup...")
            time.sleep(5) # Analysis modal

            # Identify result
            # Case A: Success
            # Case B: Captcha?
            # Case C: Quota
            
            src = self.driver.page_source
            if "quota" in src.lower():
                return 'quota_reached'
            
            if "Indexing requested" in src or "Submitted" in src:
                 return True

            # If we got here, maybe click "Got it"
            try:
                got_it = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Got it')]")
                got_it.click()
                return True
            except:
                # Ambiguous
                if "Indexing requested" in self.driver.page_source:
                    return True
                
            return False

        except Exception as e:
            print(f"❌ Exception during submission: {e}")
            return False

    def close(self):
        if self.driver:
            self.driver.quit()
