import os
import datetime
from google import genai

# ---------------- CONFIG ----------------
POSTS_DIR = "_posts"
KEYWORDS_FILE = "keywords.txt"
IMAGES_DIR = "images"

MODEL_TEXT = "gemini-1.5-flash-002"   # ✅ VALID
MODEL_IMAGE = "imagen-3.0-generate-001"

# ---------------------------------------

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_next_keyword():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    if not lines:
        print("❌ No keywords left")
        return None

    keyword = lines[0]

    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines[1:]))

    return keyword


def generate_article(title):
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
"""

    response = client.models.generate_content(
        model=MODEL_TEXT,
        contents=prompt
    )

    return response.text


def generate_image(title, filename):
    response = client.models.generate_images(
        model=MODEL_IMAGE,
        prompt=f"Professional legal blog illustration for: {title}",
        size="1024x1024"
    )

    image_bytes = response.generated_images[0].image.image_bytes
    with open(filename, "wb") as f:
        f.write(image_bytes)


def main():
    keyword = get_next_keyword()
    if not keyword:
        return

    today = datetime.date.today().strftime("%Y-%m-%d")
    slug = keyword.lower().replace(" ", "-")
    post_path = f"{POSTS_DIR}/{today}-{slug}.md"
    image_path = f"{IMAGES_DIR}/{slug}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists")
        return

    print(f"🚀 Generating article: {keyword}")
    content = generate_article(keyword)

    print("🖼 Generating image")
    generate_image(keyword, image_path)

    front_matter = f"""---
title: "{keyword}"
date: {today}
layout: post
image: /{image_path}
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(front_matter + content)

    print("✅ Post created successfully")


if __name__ == "__main__":
    main()
