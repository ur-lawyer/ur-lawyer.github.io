import os
import datetime
import requests
import time
import json
from io import BytesIO
from PIL import Image
from google import genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---------------- CONFIG ----------------
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"
SITE_DOMAIN = "https://ur-lawyer.github.io"
TEXT_MODEL = "gemini-2.5-flash"
FREEPIK_ENDPOINT = "https://api.freepik.com/v1/ai/text-to-image/flux-dev"

# How many posts to generate per run (default: 1)
# Examples: 1 = 4 posts/day | 2 = 8 posts/day | 3 = 12 posts/day
POSTS_PER_RUN = 1  # Change to 2 or 3 for faster content generation

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
FREEPIK_API_KEY = os.environ.get("FREEPIK_API_KEY")

# ---------------- HELPERS ----------------
def get_keyword_row():
    """Read and remove first line from keywords.txt"""
    if not os.path.exists(KEYWORDS_FILE):
        print(f"❌ {KEYWORDS_FILE} not found")
        return None
    
    try:
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        
        if not lines:
            print(f"📋 {KEYWORDS_FILE} is empty")
            return None
        
        row = lines.pop(0)
        print(f"📝 Removed keyword from file: {row[:50]}...")
        
        # Write remaining lines back to file
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        
        print(f"📊 Keywords remaining: {len(lines)}")
        return row
        
    except Exception as e:
        print(f"❌ Error reading keywords.txt: {e}")
        return None

def generate_article(title, focus_kw, permalink, semantic_kw):
    """Generate blog article using Gemini"""
    prompt = f"""
write an SEO-optimised blog on the title {title}. using the Focus keyword {focus_kw} and using LSI Keywords {semantic_kw}
use the following

Rules:
- Simple English, a 10 year old can understand
- Don't write more than 3 sentences per paragraph, changes paragraph after 3 sentences
- Use "you" to address the reader
- do not hightlight keywords
- Include practical examples related to {focus_kw}
- Use H2 and H3, h4, h5, h6 headings, no H1
- Use lists, tables, snippets, and other data formats
- Write more than 1500 words
- Write in Jekyll markdown format
- Naturally include focused & semantic keywords
- use author: Mary
- do not add tags only categories as {focus_kw}
- use title: {title}
- use image as image: '/images/{permalink}.webp'
"""
    
    print("🤖 Generating article with Gemini...")
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    return response.text

def generate_image_prompt(title):
    """Generate image prompt using Gemini"""
    prompt = f"""
Create a photorealistic featured image prompt for this blog post:
Title: {title}

Requirements:
- Professional, high-quality
- NO text or words in the image
- Suitable as a blog featured image
- 16:9 aspect ratio
- Relevant to the topic

Return ONLY the image prompt, nothing else.
"""
    
    print("🎨 Generating image prompt...")
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    return response.text.strip()

def generate_image_freepik(prompt, output_path):
    """Generate image using Freepik AI with polling"""
    import time
    
    if not FREEPIK_API_KEY:
        raise ValueError("❌ FREEPIK_API_KEY environment variable is not set")
    
    print(f"🔑 API Key length: {len(FREEPIK_API_KEY)} chars")
    
    headers = {
        "x-freepik-api-key": FREEPIK_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Image size options (all 16:9 aspect ratio):
    # "1920x1080" - Full HD (default)
    # "1280x720"  - HD (faster, smaller file)
    # "2560x1440" - 2K (higher quality)
    # "3840x2160" - 4K (best quality, slower)
    
    payload = {
        "prompt": prompt,
        "num_images": 1,
        "image": {
            "size": "1920x1080"  # 16:9 aspect ratio
        },
        "aspect_ratio": "widescreen_16_9"
    }
    
    print(f"📤 Sending request to Freepik API...")
    print(f"📝 Prompt: {prompt[:100]}...")
    
    try:
        # Step 1: Submit generation request
        response = requests.post(
            FREEPIK_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 401:
            print(f"❌ Authentication failed")
            raise Exception("Invalid Freepik API key")
        
        if response.status_code == 402:
            raise Exception("Freepik API credits exhausted")
        
        response.raise_for_status()
        
        # Parse initial response
        data = response.json()
        print(f"📦 Response: {data}")
        
        # Extract task_id from response
        task_id = None
        if "data" in data and isinstance(data["data"], dict):
            task_id = data["data"].get("task_id")
        
        if not task_id:
            raise Exception(f"No task_id in response: {data}")
        
        print(f"🎫 Task ID: {task_id}")
        print(f"⏳ Polling for result (this may take 30-60 seconds)...")
        
        # Step 2: Poll for result
        max_attempts = 40  # 40 attempts × 5 seconds = 200 seconds (3+ minutes)
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            time.sleep(5)  # Wait 5 seconds between polls
            
            print(f"🔄 Polling attempt {attempt}/{max_attempts}...")
            
            # Get task status - correct endpoint format
            status_url = f"https://api.freepik.com/v1/ai/text-to-image/flux-dev/{task_id}"
            print(f"🔍 Checking status at: {status_url}")
            status_response = requests.get(
                status_url,
                headers={"x-freepik-api-key": FREEPIK_API_KEY},
                timeout=30
            )
            
            status_response.raise_for_status()
            status_data = status_response.json()
            
            print(f"📊 Full status response: {status_data}")
            print(f"📊 Status: {status_data.get('data', {}).get('status', 'UNKNOWN')}")
            
            # Check if generation is complete
            if "data" in status_data and isinstance(status_data["data"], dict):
                status = status_data["data"].get("status")
                
                if status == "COMPLETED":
                    # Extract image URL
                    generated = status_data["data"].get("generated", [])
                    
                    # Check if generated is a list of URLs directly
                    if isinstance(generated, list) and len(generated) > 0:
                        # Direct list of URLs
                        image_url = generated[0] if isinstance(generated[0], str) else generated[0].get("url")
                    # Or if it's a dict with images key
                    elif isinstance(generated, dict):
                        images = generated.get("images", [])
                        if images and len(images) > 0:
                            image_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
                        else:
                            image_url = None
                    else:
                        image_url = None
                    
                    if image_url:
                        print(f"✅ Generation complete!")
                        print(f"🖼️ Image URL: {image_url[:60]}...")
                        print(f"📥 Downloading image...")
                        
                        img_response = requests.get(image_url, timeout=60)
                        img_response.raise_for_status()
                        
                        print(f"💾 Converting and saving image...")
                        img = Image.open(BytesIO(img_response.content)).convert("RGB")
                        img.save(output_path, "WEBP", quality=85)
                        
                        print(f"✅ Image saved: {output_path}")
                        return
                    else:
                        raise Exception(f"No URL found in completed response: {status_data}")
                
                elif status == "FAILED":
                    error_msg = status_data["data"].get("error", "Unknown error")
                    raise Exception(f"Generation failed: {error_msg}")
                
                elif status in ["CREATED", "PROCESSING"]:
                    # Still processing, continue polling
                    continue
                else:
                    raise Exception(f"Unknown status: {status}")
        
        # Timeout after max attempts
        raise Exception(f"Generation timeout after {max_attempts * 5} seconds")
        
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out")
        raise Exception("Freepik API request timed out")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

def submit_to_google_indexing(url):
    """
    Submit URL to Google Indexing API for immediate crawling
    """
    credentials_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    
    if not credentials_json:
        print("⚠️ GOOGLE_SERVICE_ACCOUNT_JSON not found - skipping Google indexing")
        print("💡 To enable auto-indexing, add this secret in GitHub Settings → Secrets")
        return False
    
    try:
        print(f"🔐 Parsing service account credentials...")
        credentials_info = json.loads(credentials_json)
        
        # Validate required fields
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in credentials_info]
        
        if missing_fields:
            print(f"❌ Invalid service account JSON - missing fields: {', '.join(missing_fields)}")
            print(f"💡 Please download a fresh JSON key from Google Cloud Console")
            return False
        
        print(f"📝 Service account: {credentials_info.get('client_email', 'unknown')}")
        print(f"📝 Project: {credentials_info.get('project_id', 'unknown')}")
        
        print(f"🔧 Creating credentials object...")
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/indexing']
        )
        
        print(f"🔨 Building Google Indexing API service...")
        service = build('indexing', 'v3', credentials=credentials)
        
        body = {
            'url': url,
            'type': 'URL_UPDATED'
        }
        
        print(f"📤 Submitting URL to Google Search Console...")
        print(f"🔗 URL: {url}")
        response = service.urlNotifications().publish(body=body).execute()
        
        print(f"✅ Successfully submitted to Google!")
        print(f"📋 Response: {response}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in GOOGLE_SERVICE_ACCOUNT_JSON")
        print(f"   Error: {e}")
        print(f"💡 Make sure you copied the ENTIRE JSON file contents")
        return False
    except Exception as e:
        print(f"❌ Error submitting to Google: {e}")
        print(f"💡 Common issues:")
        print(f"   1. Indexing API not enabled in Google Cloud Console")
        print(f"   2. Service account email not added as owner in Search Console")
        print(f"   3. Invalid or incomplete JSON credentials")
        print(f"   4. Check that your JSON has all required fields")
        return False

# ---------------- MAIN ----------------
def main():
    print("=" * 60)
    print("🚀 Starting Blog Post Generator")
    print("=" * 60)
    
    # Verify environment variables
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment variables")
        return
    else:
        print("✅ GEMINI_API_KEY found")
    
    if not FREEPIK_API_KEY:
        print("❌ FREEPIK_API_KEY not found in environment variables")
        return
    else:
        print("✅ FREEPIK_API_KEY found")
    
    print(f"\n📊 Posts to generate this run: {POSTS_PER_RUN}")
    
    # Show keywords file status
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            all_lines = [l.strip() for l in f if l.strip()]
        print(f"📋 Keywords available: {len(all_lines)}")
        if all_lines:
            print(f"📄 Next keyword: {all_lines[0][:80]}...")
    else:
        print(f"❌ {KEYWORDS_FILE} not found!")
    
    # Process multiple keywords based on POSTS_PER_RUN
    posts_generated = 0
    
    for post_num in range(1, POSTS_PER_RUN + 1):
        print(f"\n{'=' * 60}")
        print(f"📝 Processing Post {post_num}/{POSTS_PER_RUN}")
        print("=" * 60)
        
        # Get next keyword
        row = get_keyword_row()
        if not row:
            print(f"❌ No more keywords left in keywords.txt")
            if posts_generated == 0:
                print("⚠️ No posts were generated this run")
            else:
                print(f"✅ Generated {posts_generated} post(s) before running out of keywords")
            break
        
        print(f"\n📋 Processing keyword row:")
        print(f"   {row}")
        
        # Parse keyword row
        try:
            parts = [x.strip() for x in row.split("|")]
            if len(parts) != 4:
                print(f"❌ Invalid format. Expected 4 fields, got {len(parts)}")
                print(f"   Format: Title | Focus KW | Permalink | Semantic KW")
                continue
            
            title, focus_kw, permalink, semantic_kw = parts
            print(f"\n✅ Parsed successfully:")
            print(f"   📰 Title: {title}")
            print(f"   🎯 Focus KW: {focus_kw}")
            print(f"   🔗 Permalink: {permalink}")
            print(f"   🏷️  Semantic KW: {semantic_kw}")
        except ValueError as e:
            print(f"❌ Error parsing keyword: {e}")
            continue
        
        # Generate file paths
        today = datetime.date.today().isoformat()
        post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
        image_file = f"{IMAGES_DIR}/{permalink}.webp"
        
        # Check if post already exists
        if os.path.exists(post_path):
            print(f"\n⚠️  Post already exists: {post_path}")
            print(f"   This keyword was already processed, continuing to next...")
            # Note: The keyword has already been removed from keywords.txt by get_keyword_row()
            continue
        
        print(f"\n📝 Output files:")
        print(f"   Post: {post_path}")
        print(f"   Image: {image_file}")
        
        # Generate content
        try:
            print(f"\n{'=' * 60}")
            print("Step 1: Generating Article")
            print("=" * 60)
            article = generate_article(title, focus_kw, permalink, semantic_kw)
            print(f"✅ Article generated ({len(article)} characters)")
            
            print(f"\n{'=' * 60}")
            print("Step 2: Generating Image Prompt")
            print("=" * 60)
            image_prompt = generate_image_prompt(title)
            print(f"✅ Image prompt generated")
            
            print(f"\n{'=' * 60}")
            print("Step 3: Generating Image via Freepik AI")
            print("=" * 60)
            generate_image_freepik(image_prompt, image_file)
            
            print(f"\n{'=' * 60}")
            print("Step 4: Saving Post")
            print("=" * 60)
            with open(post_path, "w", encoding="utf-8") as f:
                f.write(article)
            print(f"✅ Post saved: {post_path}")
            
            # Construct the full URL for the post
            post_url = f"{SITE_DOMAIN}/{permalink}/"
            
            print(f"\n{'=' * 60}")
            print(f"✅ SUCCESS! Post {post_num} Generated")
            print("=" * 60)
            print(f"📰 Title: {title}")
            print(f"📄 File: {post_path}")
            print(f"🖼️  Image: {image_file}")
            print(f"🌐 URL: {post_url}")
            
            posts_generated += 1
            
            # Wait 5 minutes before submitting to Google (only for the last post)
            if post_num == POSTS_PER_RUN or post_num == posts_generated:
                print(f"\n{'=' * 60}")
                print("Step 5: Waiting 5 minutes before submitting to Google")
                print("=" * 60)
                print("⏳ This allows GitHub Pages to deploy the post(s) first...")
                
                # Wait 5 minutes (300 seconds)
                wait_time = 300
                for remaining in range(wait_time, 0, -30):
                    minutes = remaining // 60
                    seconds = remaining % 60
                    print(f"⏰ Time remaining: {minutes}m {seconds}s", end='\r')
                    time.sleep(30)
                
                print(f"\n✅ Wait complete!")
                
                print(f"\n{'=' * 60}")
                print("Step 6: Submitting to Google Search Console")
                print("=" * 60)
                
                try:
                    submit_to_google_indexing(post_url)
                except Exception as e:
                    print(f"⚠️ Google submission failed (non-critical): {e}")
                    print(f"💡 Post was still published successfully!")
                    print(f"🔗 You can manually submit: {post_url}")
            
        except Exception as e:
            print(f"\n{'=' * 60}")
            print(f"❌ FAILED: {e}")
            print("=" * 60)
            print(f"⚠️ Continuing to next keyword...")
            continue
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("🎉 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Posts generated this run: {posts_generated}")
    print(f"📊 Keywords remaining: Check keywords.txt")

if __name__ == "__main__":
    main()