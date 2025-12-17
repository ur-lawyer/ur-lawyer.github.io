import os
import datetime
from google import genai

# ---------------- CONFIG ----------------
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"
TEXT_MODEL = "gemini-2.5-flash"
IMAGE_SIZE = (1920, 1080)

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ---------------- HELPERS ----------------
def get_keyword_row():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return None

    row = lines.pop(0)
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return row


def generate_article(title, focus_kw, permalink, semantic_kw):
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

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    return response.text


def generate_image_prompt(title):
    prompt = f"""
Create a detailed AI image prompt for a blog featured image.

Blog Title: {title}

Rules:
- Photorealistic
- Professional blog style
- No text in image
- 16:9 composition
"""

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt,
        size=IMAGE_SIZE
    )
    return response.text.strip()


# ---------------- MAIN ----------------
def main():
    row = get_keyword_row()
    if not row:
        print("❌ No keywords left")
        return

    try:
        title, focus_kw, permalink, semantic_kw = [x.strip() for x in row.split("|")]
    except ValueError:
        print("❌ Invalid keyword format")
        return

    today = datetime.date.today().isoformat()
    post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    image_path = f"/images/{permalink}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists")
        return

    print(f"✍️ Generating post: {title}")

    article = generate_article(title, focus_kw, permalink, semantic_kw)
    image_prompt = generate_image_prompt(title)

    front_matter = f"""---
title: "{title}"
date: {today}
image: {image_path}
focus_keyword: "{focus_kw}"
semantic_keywords: "{semantic_kw}"
image_prompt: "{image_prompt}"
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(article)

    print("✅ Post generated successfully")


if __name__ == "__main__":
    main()
