import os
import datetime
import google.generativeai as genai
from PIL import Image, ImageDraw
import textwrap

# ---------------- CONFIG ----------------
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"
MODEL_NAME = "gemini-1.5-flash"
# ----------------------------------------

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


def read_keywords():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                return [x.strip() for x in line.split("|")]
    return None


def remove_used_keyword(used_line):
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if used_line not in line:
                f.write(line)


def generate_article(title, focus_kw, semantic_kw):
    model = genai.GenerativeModel(MODEL_NAME)

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

    response = model.generate_content(prompt)
    return response.text


def generate_image(text, output_path):
    img = Image.new("RGB", (800, 1000), color="#111111")  # 4:5 ratio
    draw = ImageDraw.Draw(img)

    wrapped = textwrap.fill(text, 22)
    draw.text((40, 400), wrapped, fill="white")

    img.save(output_path, "WEBP")


def main():
    data = read_keywords()
    if not data:
        print("❌ No keywords left")
        return

    title, focus_kw, permalink, semantic_kw = data
    today = datetime.date.today().isoformat()

    post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    image_path = f"{IMAGES_DIR}/{permalink}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists")
        return

    print(f"🚀 Generating: {title}")

    content = generate_article(title, focus_kw, semantic_kw)

    generate_image(title, image_path)

    front_matter = f"""---
title: "{title}"
date: {today}
layout: post
image: /images/{permalink}.webp
tags: [{semantic_kw}]
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(front_matter + content)

    remove_used_keyword("|".join(data))

    print("✅ Post & image generated")


if __name__ == "__main__":
    main()
