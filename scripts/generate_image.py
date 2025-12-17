import google.generativeai as genai
import os
from PIL import Image
from io import BytesIO

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_image(title, permalink):
    prompt = f"""
Create a professional featured image for a legal blog article.

Article title: {title}

Style rules:
- Photorealistic or realistic illustration
- Professional law office or consultation scene
- Neutral colors
- Modern lighting
- No text
- No logos
- Vertical composition
"""

    response = genai.generate_images(
        model="imagen-3.0-generate-001",
        prompt=prompt,
        size="1024x1280"   # ✅ 4:5 aspect ratio
    )

    image_bytes = response.images[0].image_bytes
    image = Image.open(BytesIO(image_bytes))

    # Safety resize (ensures exact ratio)
    image = image.resize((1024, 1280), Image.LANCZOS)

    image_path = os.path.join(IMAGE_DIR, f"{permalink}.webp")
    image.save(image_path, "WEBP", quality=90)

    print(f"🖼️ Image generated: {image_path}")

    return f"/images/{permalink}.webp"


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


How Long Do Personal Injury Lawsuits Take? What You Need to Know | personal injury lawyer | how-long-do-personal-injury-lawsuits-take | Lawyer near me
