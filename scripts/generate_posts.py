import os
import datetime
import requests
from io import BytesIO
from PIL import Image
from google import genai

# ---------------- CONFIG ----------------
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"
TEXT_MODEL = "gemini-2.5-flash"
FREEPIK_ENDPOINT = "https://api.freepik.com/v1/ai/text-to-image/flux-dev"

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
        
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    if not lines:
        return None
    
    row = lines.pop(0)
    
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:  # Add trailing newline if there are remaining lines
            f.write("\n")
    
    return row

def generate_article(title, focus_kw, permalink, semantic_kw):
    """Generate blog article using Gemini"""
    prompt = f"""
write an SEO-optimised blog on the title {title}. using the Focus keyword {focus_kw} and using LSI Keywords {semantic_kw}
use the following

Rules:
- Simple English
- Max 3 sentences per paragraph
- Use "you" to address the reader
- Include practical examples related to {focus_kw}
- Use H2 and H3, h4, h5, h6 headings, no H1
- Use lists, tables, snippets, and other data formats
- Write more than 2000 words
- Write in Jekyll markdown format
- Naturally include focused & semantic keywords
- use author: Mary
- do not add tags only categories as {focus_kw}
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
    """Generate image using Freepik AI"""
    if not FREEPIK_API_KEY:
        raise ValueError("❌ FREEPIK_API_KEY environment variable is not set")
    
    print(f"🔑 API Key length: {len(FREEPIK_API_KEY)} chars")
    
    headers = {
        "x-freepik-api-key": FREEPIK_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Simplified payload for better compatibility
    payload = {
        "prompt": prompt,
        "num_images": 1,
        "image": {
            "size": "1920x1080"
        }
    }
    
    print(f"📤 Sending request to Freepik API...")
    print(f"📝 Prompt: {prompt[:100]}...")
    
    try:
        response = requests.post(
            FREEPIK_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=180  # 3 minutes timeout
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 401:
            print(f"❌ Authentication failed")
            print(f"Response: {response.text}")
            raise Exception("Invalid Freepik API key. Verify at https://www.freepik.com/api")
        
        if response.status_code == 402:
            print(f"❌ Payment required")
            raise Exception("Freepik API credits exhausted")
        
        if response.status_code == 400:
            print(f"❌ Bad request")
            print(f"Response: {response.text}")
            raise Exception(f"Invalid parameters: {response.text}")
        
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        print(f"📦 Response keys: {list(data.keys())}")
        
        # Try to find image URL in different response formats
        image_url = None
        
        if isinstance(data, dict):
            # Format 1: {"data": [{"url": "..."}]}
            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                image_url = data["data"][0].get("url")
            # Format 2: {"data": {"url": "..."}}
            elif "data" in data and isinstance(data["data"], dict):
                image_url = data["data"].get("url")
            # Format 3: {"url": "..."}
            elif "url" in data:
                image_url = data["url"]
            # Format 4: {"image": "..."}
            elif "image" in data:
                image_url = data["image"]
        
        if not image_url:
            print(f"❌ Could not find image URL in response")
            print(f"Full response: {data}")
            raise Exception(f"Unexpected API response structure: {data}")
        
        print(f"🖼️ Image URL found: {image_url[:50]}...")
        print(f"📥 Downloading image...")
        
        img_response = requests.get(image_url, timeout=60)
        img_response.raise_for_status()
        
        print(f"💾 Converting and saving image...")
        img = Image.open(BytesIO(img_response.content)).convert("RGB")
        img.save(output_path, "WEBP", quality=85)
        
        print(f"✅ Image saved: {output_path}")
        
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
    
    # Get next keyword
    row = get_keyword_row()
    if not row:
        print("❌ No keywords left in keywords.txt")
        return
    
    print(f"\n📋 Processing keyword row:")
    print(f"   {row}")
    
    # Parse keyword row
    try:
        parts = [x.strip() for x in row.split("|")]
        if len(parts) != 4:
            print(f"❌ Invalid format. Expected 4 fields, got {len(parts)}")
            print(f"   Format: Title | Focus KW | Permalink | Semantic KW")
            return
        
        title, focus_kw, permalink, semantic_kw = parts
        print(f"\n✅ Parsed successfully:")
        print(f"   📰 Title: {title}")
        print(f"   🎯 Focus KW: {focus_kw}")
        print(f"   🔗 Permalink: {permalink}")
        print(f"   🏷️  Semantic KW: {semantic_kw}")
    except ValueError as e:
        print(f"❌ Error parsing keyword: {e}")
        return
    
    # Generate file paths
    today = datetime.date.today().isoformat()
    post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    image_file = f"{IMAGES_DIR}/{permalink}.webp"
    
    # Check if post already exists
    if os.path.exists(post_path):
        print(f"\n⚠️  Post already exists: {post_path}")
        return
    
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
        
        print(f"\n{'=' * 60}")
        print("✅ SUCCESS! Post + Image published")
        print("=" * 60)
        print(f"📰 Title: {title}")
        print(f"📄 File: {post_path}")
        print(f"🖼️  Image: {image_file}")
        
    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"❌ FAILED: {e}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    main()