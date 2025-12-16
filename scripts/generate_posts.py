import os
import datetime
import requests
import base64

# ================= CONFIG =================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"

MODEL_TEXT = "gemini-1.5-flash"
MODEL_IMAGE = "imagen-3.0-generate-002"

# =========================================

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def call_gemini_text(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_TEXT}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

def generate_image(prompt, filename):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_IMAGE}:generateImages?key={GEMINI_API_KEY}"
    payload = {
        "prompt": prompt,
        "aspectRatio": "4:5",
        "mimeType": "image/webp"
    }
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    img_base64 = r.json()["images"][0]["bytesBase64Encoded"]
    with open(filename, "wb") as f:
        f.write(base64.b64decode(img_base64))

def main():
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not found")

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        print("⚠️ No keywords left")
        return

    # Process ONLY ONE keyword per run
    line = lines[0]
    title, focus_kw, permalink, semantic_kw = [x.strip() for x in line.split("|")]

    today = datetime.date.today().strftime("%Y-%m-%d")
    post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    image_path = f"{IMAGES_DIR}/{permalink}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists, skipping")
        return

    print(f"📝 Generating article: {title}")

    article_prompt = f"""
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
"""

    content = call_gemini_text(article_prompt)

    image_prompt = f"""
Professional legal blog featured image.
Topic: {title}
Style: clean, modern, law office, justice theme
No text on image
"""

    print("🖼️ Generating image...")
    generate_image(image_prompt, image_path)

    front_matter = f"""---
title: "{title}"
date: {today}
layout: post
image: /images/{permalink}.webp
focus_keyword: "{focus_kw}"
tags: [{semantic_kw}]
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(front_matter + content)

    # Remove used keyword
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        for l in lines[1:]:
            f.write(l + "\n")

    print("✅ Post and image generated successfully")

if __name__ == "__main__":
    main()
