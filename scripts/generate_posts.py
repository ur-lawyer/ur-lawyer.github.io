import os
import datetime
import urllib.parse
import requests
from io import BytesIO
from PIL import Image
import google.generativeai as genai

# ================= CONFIG =================
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"

MODEL_NAME = "gemini-2.5-flash"
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080  # 16:9 aspect ratio
# ==========================================

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)


def get_next_keyword():
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        return None

    first = lines[0]
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines[1:]))

    return first


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
    response = model.generate_content(prompt)
    return response.text


def generate_image(title, image_path):
    prompt = f"Professional blog illustration, {title}, legal theme, clean, modern, realistic"
    encoded = urllib.parse.quote(prompt)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&seed=42"
    )

    print("🖼️ Generating image via Pollinations AI")
    r = requests.get(url, timeout=120)
    r.raise_for_status()

    img = Image.open(BytesIO(r.content)).convert("RGB")
    img.save(image_path, "WEBP", quality=85)


def main():
    row = get_next_keyword()
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
    image_path = f"{IMAGES_DIR}/{permalink}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists")
        return

    print(f"✍️ Generating post: {title}")

    content = generate_article(title, focus_kw, permalink, semantic_kw)
    generate_image(title, image_path)

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Post published successfully")


if __name__ == "__main__":
    main()
