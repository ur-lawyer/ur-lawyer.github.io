#!/usr/bin/env python3
"""
Extract Google authentication cookies from Chrome profile
Creates a minimal cookie file for GitHub Secrets storage
"""
import os
import sys
import json
import base64
import sqlite3
import shutil
from pathlib import Path

def extract_google_cookies(profile_path):
    """Extract Google cookies from Chrome profile"""
    
    cookies_db = os.path.join(profile_path, "Default", "Cookies")
    
    if not os.path.exists(cookies_db):
        print(f"❌ Cookies database not found at: {cookies_db}")
        return None
    
    # Copy cookies DB (Chrome locks it)
    temp_cookies = "/tmp/cookies_copy.db"
    shutil.copy2(cookies_db, temp_cookies)
    
    try:
        conn = sqlite3.connect(temp_cookies)
        cursor = conn.cursor()
        
        # Extract Google-related cookies
        query = """
        SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
        FROM cookies 
        WHERE host_key LIKE '%google.com%'
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        cookies = []
        for row in rows:
            cookie = {
                'domain': row[0],
                'name': row[1],
                'value': row[2],
                'path': row[3],
                'expires': row[4],
                'secure': bool(row[5]),
                'httpOnly': bool(row[6])
            }
            cookies.append(cookie)
        
        conn.close()
        os.unlink(temp_cookies)
        
        return cookies
        
    except Exception as e:
        print(f"❌ Error extracting cookies: {e}")
        if os.path.exists(temp_cookies):
            os.unlink(temp_cookies)
        return None


def main():
    print("=" * 60)
    print("🍪 Google Cookie Extraction for GitHub Secrets")
    print("=" * 60)
    
    profile_path = os.path.join(os.path.expanduser("~"), ".gsc_chrome_profile")
    
    if not os.path.exists(profile_path):
        print(f"\n❌ Chrome profile not found!")
        print(f"   Expected: {profile_path}")
        print(f"\n💡 Run first_time_gsc_login.py first")
        sys.exit(1)
    
    print(f"\n📁 Profile: {profile_path}")
    print(f"🔍 Extracting Google cookies...")
    
    cookies = extract_google_cookies(profile_path)
    
    if not cookies:
        sys.exit(1)
    
    print(f"✅ Extracted {len(cookies)} Google cookies")
    
    # Convert to JSON
    cookies_json = json.dumps(cookies, indent=2)
    cookies_size = len(cookies_json)
    
    print(f"📊 Cookie data size: {cookies_size / 1024:.2f} KB")
    
    if cookies_size > 60000:  # Leave some margin under 64KB
        print(f"⚠️  Warning: Cookies are close to 64KB limit!")
    
    # Encode for GitHub Secrets
    encoded = base64.b64encode(cookies_json.encode()).decode()
    encoded_size = len(encoded)
    
    print(f"📊 Encoded size: {encoded_size / 1024:.2f} KB")
    
    if encoded_size > 64000:
        print(f"❌ Encoded cookies exceed 64KB GitHub Secret limit!")
        print(f"   Try removing some cookies or use API fallback")
        sys.exit(1)
    
    # Save to file
    output_file = "gsc_cookies_encoded.txt"
    with open(output_file, 'w') as f:
        f.write(encoded)
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"\n" + "=" * 60)
    print("📋 NEXT STEPS:")
    print("=" * 60)
    print("1. Copy contents of gsc_cookies_encoded.txt")
    print("2. GitHub → Settings → Secrets → Actions")
    print("3. Create secret: GSC_COOKIES")
    print("4. Paste the encoded cookies")
    print("5. Delete gsc_cookies_encoded.txt (sensitive!)")
    print("=" * 60)


if __name__ == "__main__":
    main()
