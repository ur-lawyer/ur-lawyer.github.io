
import os
import base64
from datetime import date
from google import genai
from PIL import Image, ImageDraw

# ================= CONFIG =================
KEYWORDS_FILE = "keywords.txt"
POSTS_DIR = "_posts"
IMAGES_DIR = "images"

TEXT_MODEL = "gemini-2.5-flash"   # ✅ VALID MODEL
IMAGE_SIZE = (1024, 1280)

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ================= HELPERS =================
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
    return f"""
Ultra high-quality blog cover image for:
"{title}"

Style:
- Professional blog hero image
- Clean, modern, premium
- Cinematic lighting
- High contrast
- No text or letters

Composition:
- Center subject
- Topic-relevant
- 4:5 ratio
"""


def generate_image(title, image_path):
    prompt = generate_image_prompt(title)

    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=IMAGE_SIZE
    )

    image_base64 = img.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(image_path, "wb") as f:
        f.write(image_bytes)


# ================= MAIN =================
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

    today = date.today().isoformat()
    post_path = f"{POSTS_DIR}/{today}-{permalink}.md"
    image_path = f"{IMAGES_DIR}/{permalink}.webp"

    if os.path.exists(post_path):
        print("⚠️ Post already exists")
        return

    print(f"📝 Generating post: {title}")

    content = generate_article(title, focus_kw, semantic_kw)
    generate_image(title, image_path)


    with open(post_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Post & image generated successfully")


if __name__ == "__main__":
    main()
