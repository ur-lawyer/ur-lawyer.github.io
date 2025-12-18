"""Generate blog articles using Gemini AI"""
from google import genai
from config import TEXT_MODEL, GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_article(title, focus_kw, permalink, semantic_kw):
    """Generate SEO-optimized blog article"""
    prompt = f"""
write an SEO-optimised blog on the title {title}. using the Focus keyword {focus_kw} and using LSI Keywords {semantic_kw}
use the following

Rules:
- Simple English, a 10 year old can understand
- Don't write more than 3 sentences per paragraph, changes paragraph after 3 sentences
- Use "you" to address the reader
- if need use legal websites link to refer to legal information
- do not highlight keywords
- Include practical examples related to {focus_kw}
- Use H2 and H3, h4, h5, h6 headings, no H1
- Use lists, tables, snippets, and other data formats
- Write more than 1500 words
- Write in Jekyll markdown format
- Naturally include focused & semantic keywords
- use the following front matter only:
layout: post
title: {title}
description: "article description in less than 160 characters"
author: Mary
tags: {focus_kw}
featured: false
image: '/images/{permalink}.webp'
"""
    
    print("🤖 Generating article with Gemini...")
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    return response.text


def generate_image_prompt(title):
    """Generate image prompt for Freepik AI"""
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