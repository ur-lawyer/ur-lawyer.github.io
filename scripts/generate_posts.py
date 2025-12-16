import os
import datetime
from google import genai
from PIL import Image, ImageDraw
import textwrap

KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"
MODEL = "models/gemini-1.5-flash"

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_keyword():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                return line.strip(), [x.strip() for x in line.split("|")]
    return None, None


def remove_keyword(line):
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        for l in lines:
            if l.strip() != line:
                f.write(l)


def generate_article(title, focus_kw, semantic_kw):
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
        model=MODEL,
        contents=prompt,
    )

    return response.text


def generate_image(text, path):
    img = Image.new("RGB", (800, 1000), "#111111")  # 4:5 ratio
    draw = ImageDraw.Draw(img)
    wrapped = textwrap.fill(text, 22)
    draw.text((40, 400), wrapped, fill="white")
    img.save(path, "WEBP")


def main():
    line, data = get_keyword()
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

    remove_keyword(line)
    print("✅ Post published")


if __name__ == "__main__":
    main()




import os
import datetime
from google import genai
from PIL import Image, ImageDraw

# ---------------- CONFIG ----------------
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"

TEXT_MODEL = "gemini-1.5-flash-002"   # ✅ VALID MODEL
IMAGE_SIZE = (1200, 630)

# ---------------------------------------

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_keyword():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        return None

    keyword = lines[0]

    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines[1:]))

    return keyword


def generate_article(title, focus_kw, semantic_kw):
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
        model=TEXT_MODEL,
        contents=prompt
    )

    return response.text


def generate_image(title, path):
    img = Image.new("RGB", IMAGE_SIZE, "#f4f4f4")
    draw = ImageDraw.Draw(img)
    draw.text((40, 250), title[:80], fill="#000")
    img.save(path, "WEBP")


def main():
    data = get_keyword()
    if not data:
        print("❌ No keywords left")
        return

    title, focus_kw, permalink, semantic_kw = data.split("|")

    today = datetime.date.today().strftime("%Y-%m-%d")
    post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    image_path = f"{IMAGES_DIR}/{permalink}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists")
        return

    print(f"🚀 Generating post: {title}")

    content = generate_article(title, focus_kw, semantic_kw)
    generate_image(title, image_path)

    front_matter = f"""---
title: "{title}"
date: {today}
layout: post
image: /{image_path}
keywords: [{semantic_kw}]
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(front_matter + content)

    print("✅ Post published successfully")


if __name__ == "__main__":
    main()
