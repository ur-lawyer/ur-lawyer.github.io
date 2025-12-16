
import os
import google.generativeai as genai
from datetime import datetime

# ---------------- CONFIG ----------------

KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"

# Ensure posts directory exists
os.makedirs(POSTS_DIR, exist_ok=True)

# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("❌ GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_API_KEY)

# Stable & fast Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- FUNCTIONS ----------------

def generate_blog_content(title, focus_kw, permalink, semantic_kw):
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
    return response.text.strip()

# ---------------- MAIN ----------------

with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for line in lines[:8]:  # Max 8 posts per run
    try:
        # Expected format:
        # title,focus keyword,semantic keywords,permalink
        title, focus_kw, permalink, semantic_kw = line.split(",", 3)

        date = datetime.utcnow()
        date_str = date.strftime("%Y-%m-%d")
        full_date = date.strftime("%Y-%m-%d %H:%M:%S +0000")

        filename = f"{POSTS_DIR}/{date_str}-{permalink}.md"

        # Prevent duplicate posts
        if os.path.exists(filename):
            print(f"⏭️ Skipping existing post: {filename}")
            continue

        print(f"✍️ Generating: {title}")

        content = generate_blog_content(title, focus_kw, permalink, semantic_kw)

        front_matter = f"""---
layout: post
title: "{title}"
date: {full_date}
description: "{title} – complete guide and detailed explanation."
tags: [{focus_kw}]
---

"""

        with open(filename, "w", encoding="utf-8") as post:
            post.write(front_matter)
            post.write(content)

        print(f"✅ Published: {filename}")

    except Exception as e:
        print(f"❌ Error processing line: {line}")
        print(e)
