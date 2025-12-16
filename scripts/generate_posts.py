import os
from datetime import datetime
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = genai.GenerativeModel("gemini-2.5-flash")
POSTS_PER_DAY = 8
POST_DIR = "_posts"

with open("keywords.txt", "r") as f:
    rows = [line.strip() for line in f if line.count("|") == 3]

today = datetime.utcnow().strftime("%Y-%m-%d")

def generate_post(title, focus_kw, permalink, semantic_kw):
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

    response = MODEL.generate_content(prompt)
    return response.text


for row in rows[:POSTS_PER_DAY]:
    title, focus_kw, permalink, semantic_kw = [x.strip() for x in row.split("|")]

    filename = f"{POST_DIR}/{today}-{permalink}.md"

    content = generate_post(title, focus_kw, permalink, semantic_kw)

    markdown = f"""---
title: "{title}"
permalink: /{permalink}/
description: "{focus_kw.capitalize()} – complete guide, honest answers, and expert insights."
date: {today}
categories: blog
keywords: [{semantic_kw}]
---

{content}
"""

    with open(filename, "w") as f:
        f.write(markdown)

print("✅ 8 Gemini-powered SEO posts generated")
