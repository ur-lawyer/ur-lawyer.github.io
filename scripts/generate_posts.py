"""Main script to generate blog posts automatically"""
import os
import time
import datetime

# Import all modules
from config import *
from keywords_handler import get_keyword_row, remove_keyword_from_file, get_keywords_count
from article_generator import generate_article, generate_image_prompt
from image_generator import generate_image_freepik
from google_indexing import submit_to_google_indexing
from google_sheets_logger import log_to_google_sheets


def main():
    print("=" * 60)
    print("🚀 Starting Blog Post Generator")
    print("=" * 60)
    
    # Verify environment variables
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found")
        return
    print("✅ GEMINI_API_KEY found")
    
    if not FREEPIK_API_KEY:
        print("❌ FREEPIK_API_KEY not found")
        return
    print("✅ FREEPIK_API_KEY found")
    
    # Show keywords status
    keywords_count = get_keywords_count()
    print(f"\n📊 Posts to generate this run: {POSTS_PER_RUN}")
    print(f"📋 Keywords available: {keywords_count}")
    
    posts_generated = 0
    
    for post_num in range(1, POSTS_PER_RUN + 1):
        print(f"\n{'=' * 60}")
        print(f"📝 Processing Post {post_num}/{POSTS_PER_RUN}")
        print("=" * 60)
        
        # Get next keyword
        row = get_keyword_row()
        if not row:
            print(f"❌ No more keywords left")
            break
        
        print(f"\n📋 Keyword: {row[:80]}...")
        
        # Parse keyword
        try:
            parts = [x.strip() for x in row.split("|")]
            if len(parts) != 4:
                print(f"❌ Invalid format. Expected 4 fields, got {len(parts)}")
                remove_keyword_from_file()  # Remove invalid keyword
                continue
            
            title, focus_kw, permalink, semantic_kw = parts
            print(f"✅ Parsed: {title[:60]}...")
        except ValueError as e:
            print(f"❌ Error parsing: {e}")
            remove_keyword_from_file()
            continue
        
        # Generate file paths
        today = datetime.date.today().isoformat()
        post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
        image_file = f"{IMAGES_DIR}/{permalink}.webp"
        
        # Check if post already exists
        if os.path.exists(post_path):
            print(f"\n⚠️  Post already exists: {post_path}")
            remove_keyword_from_file()  # Remove duplicate
            continue
        
        # Generate content
        try:
            # Step 1: Generate article
            print(f"\n{'=' * 60}")
            print("Step 1: Generating Article")
            print("=" * 60)
            article = generate_article(title, focus_kw, permalink, semantic_kw)
            print(f"✅ Article generated ({len(article)} characters)")
            
            # Step 2: Generate image prompt
            print(f"\n{'=' * 60}")
            print("Step 2: Generating Image Prompt")
            print("=" * 60)
            image_prompt = generate_image_prompt(title)
            print(f"✅ Image prompt generated")
            
            # Step 3: Generate image
            print(f"\n{'=' * 60}")
            print("Step 3: Generating & Compressing Image")
            print("=" * 60)
            generate_image_freepik(image_prompt, image_file)
            
            # Step 4: Save post
            print(f"\n{'=' * 60}")
            print("Step 4: Saving Post")
            print("=" * 60)
            with open(post_path, "w", encoding="utf-8") as f:
                f.write(article)
            print(f"✅ Post saved: {post_path}")
            
            post_url = f"{SITE_DOMAIN}/{permalink}/"
            
            print(f"\n{'=' * 60}")
            print(f"✅ SUCCESS! Post {post_num} Generated")
            print("=" * 60)
            print(f"📰 Title: {title}")
            print(f"🌐 URL: {post_url}")
            
            posts_generated += 1
            
            # Step 5: Wait before indexing
            if post_num == POSTS_PER_RUN or post_num == posts_generated:
                print(f"\n{'=' * 60}")
                print(f"Step 5: Waiting {WAIT_TIME_BEFORE_INDEXING // 60} minutes")
                print("=" * 60)
                print("⏳ Allowing GitHub Pages to deploy...")
                
                for remaining in range(WAIT_TIME_BEFORE_INDEXING, 0, -30):
                    minutes = remaining // 60
                    seconds = remaining % 60
                    print(f"⏰ Time remaining: {minutes}m {seconds}s", end='\r')
                    time.sleep(30)
                
                print(f"\n✅ Wait complete!")
                
                # Step 6: Submit to Google
                print(f"\n{'=' * 60}")
                print("Step 6: Submitting to Google")
                print("=" * 60)
                
                indexing_status = "Not Attempted"
                try:
                    success = submit_to_google_indexing(post_url)
                    indexing_status = "Success" if success else "Failed - See Logs"
                except Exception as e:
                    indexing_status = f"Failed - {str(e)[:100]}"
                    print(f"⚠️ Indexing failed (non-critical): {e}")
                
                # Step 7: Log to Sheets
                print(f"\n{'=' * 60}")
                print("Step 7: Logging to Google Sheets")
                print("=" * 60)
                
                try:
                    log_to_google_sheets(
                        title, focus_kw, permalink,
                        image_file, article, indexing_status
                    )
                except Exception as e:
                    print(f"⚠️ Sheets logging failed (non-critical): {e}")
            
            # Step 8: Remove keyword after success
            print(f"\n{'=' * 60}")
            print("Step 8: Removing Keyword from File")
            print("=" * 60)
            remove_keyword_from_file()
            
        except Exception as e:
            print(f"\n{'=' * 60}")
            print(f"❌ FAILED: {e}")
            print("=" * 60)
            print(f"⚠️ Keyword NOT removed - will retry next run")
            continue
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("🎉 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Posts generated: {posts_generated}")
    print(f"📊 Keywords remaining: {get_keywords_count()}")


if __name__ == "__main__":
    main()