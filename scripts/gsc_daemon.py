#!/usr/bin/env python3
"""
GSC Auto Queue Processor with Video Recording
- Starts automatically when Mac boots
- Pulls pending URLs from GitHub
- Processes them using your gsc_automation.py (with video recording)
- Commits results back to GitHub
"""
import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
REPO_DIR = Path.home() / "Documents/ur-lawyer.github.io"
SCRIPTS_DIR = REPO_DIR / "scripts"
PENDING_FILE = REPO_DIR / "pending_gsc_urls.json"
LOG_FILE = REPO_DIR / "gsc_auto_processor.log"
CHECK_INTERVAL = 300  # Check every 5 minutes

# Add scripts directory to Python path
sys.path.insert(0, str(SCRIPTS_DIR))

def log(message):
    """Log to file and print"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

def git_pull():
    """Pull latest changes from GitHub"""
    try:
        log("📥 Pulling latest changes from GitHub...")
        result = subprocess.run(
            ['git', 'pull'],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            log("✅ Git pull successful")
            return True
        else:
            log(f"⚠️  Git pull failed: {result.stderr}")
            return False
    except Exception as e:
        log(f"❌ Git pull error: {e}")
        return False

def git_commit_and_push():
    """Commit and push changes back to GitHub"""
    try:
        log("📤 Committing and pushing changes...")
        
        # Add the pending file
        subprocess.run(['git', 'add', 'pending_gsc_urls.json'], cwd=REPO_DIR, check=True)
        
        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', 'Update GSC submission status [auto]'],
            cwd=REPO_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and 'nothing to commit' not in result.stdout:
            log(f"⚠️  Git commit failed: {result.stderr}")
            return False
        
        # Push
        result = subprocess.run(
            ['git', 'push'],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            log("✅ Changes pushed to GitHub")
            return True
        else:
            log(f"⚠️  Git push failed: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"❌ Git operation error: {e}")
        return False

def get_pending_urls():
    """Get pending URLs from JSON file"""
    if not PENDING_FILE.exists():
        return [], []
    
    try:
        with open(PENDING_FILE, 'r') as f:
            urls_data = json.load(f)
        
        pending = [u for u in urls_data if u.get('status') == 'pending']
        return pending, urls_data
    except Exception as e:
        log(f"❌ Error reading pending file: {e}")
        return [], []

def process_pending_urls():
    """Process all pending URLs using gsc_automation.py"""
    pending, urls_data = get_pending_urls()
    
    if not pending:
        log("ℹ️  No pending URLs to process")
        return False
    
    log(f"📋 Found {len(pending)} pending URLs to process")
    
    # Import GSC automation
    from gsc_automation import GSCAutomation
    
    # Initialize with video recording enabled
    # Note: record_video is not implemented in the base class yet but passed for future use
    bot = GSCAutomation(
        profile_path=str(SCRIPTS_DIR / "chrome_profile"),
        headless=False,
        record_video=True
    )
    
    try:
        # Get property ID
        property_id = bot.get_property_id("https://ur-lawyer.github.io/", use_domain_property=False)
        
        processed = 0
        
        for url_data in pending:
            log(f"\n{'='*60}")
            log(f"Processing: {url_data.get('title', 'Untitled')}")
            log(f"URL: {url_data['url']}")
            log(f"{'='*60}")
            
            result = bot.submit_url(url_data['url'], property_id)
            
            if result is True:
                url_data['status'] = 'submitted'
                url_data['submitted_at'] = datetime.now().isoformat()
                log(f"✅ Successfully submitted")
                processed += 1
            elif result == 'already_requested':
                url_data['status'] = 'already_requested'
                url_data['submitted_at'] = datetime.now().isoformat()
                log(f"✅ Already requested")
                processed += 1
            elif result == 'quota_reached':
                url_data['status'] = 'quota_reached'
                log(f"⚠️  Quota reached - stopping for now")
                break
            else:
                url_data['status'] = 'failed'
                url_data['failed_at'] = datetime.now().isoformat()
                log(f"❌ Submission failed")
            
            # Save progress after each URL
            with open(PENDING_FILE, 'w') as f:
                json.dump(urls_data, f, indent=2)
            
            # Wait between submissions
            if url_data != pending[-1]:
                log("⏳ Waiting 15 seconds before next URL...")
                time.sleep(15)
        
        log(f"\n📊 Processed {processed} URLs successfully")
        log(f"🎬 Videos saved in: {SCRIPTS_DIR}/recordings/")
        return processed > 0
        
    except Exception as e:
        log(f"❌ Error during processing: {e}")
        import traceback
        log(traceback.format_exc())
        return False
    finally:
        bot.close()
        log("🔒 Browser closed")

def main():
    """Main loop - runs continuously"""
    log("="*60)
    log("🤖 GSC Auto Queue Processor Started (with Video Recording)")
    log(f"📁 Repository: {REPO_DIR}")
    log(f"📝 Log file: {LOG_FILE}")
    log(f"🎥 Recordings: {SCRIPTS_DIR}/recordings/")
    log(f"⏱️  Check interval: {CHECK_INTERVAL}s")
    log("="*60)
    
    # Process queue immediately on startup
    log("\n🔄 Initial check for pending URLs...")
    git_pull()
    
    if process_pending_urls():
        git_commit_and_push()
        log("\n✅ Initial queue processed successfully!")
    
    # Then check periodically
    log(f"\n👀 Now monitoring for new URLs every {CHECK_INTERVAL//60} minutes...")
    
    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            
            log(f"\n🔄 Periodic check ({time.strftime('%I:%M %p')})...")
            
            # Pull latest changes
            if git_pull():
                # Process any new pending URLs
                if process_pending_urls():
                    # Push results back
                    git_commit_and_push()
                    log("✅ Queue processed and synced")
                else:
                    log("ℹ️  No new URLs to process")
            
    except KeyboardInterrupt:
        log("\n🛑 Processor stopped by user")
    except Exception as e:
        log(f"\n❌ Unexpected error: {e}")
        import traceback
        log(traceback.format_exc())

if __name__ == "__main__":
    main()
