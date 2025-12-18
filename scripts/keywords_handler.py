"""Handle reading and managing keywords.txt"""
import os
from config import KEYWORDS_FILE


def get_keyword_row():
    """Read first line from keywords.txt WITHOUT removing it"""
    if not os.path.exists(KEYWORDS_FILE):
        print(f"❌ {KEYWORDS_FILE} not found")
        return None
    
    try:
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        
        if not lines:
            print(f"📋 {KEYWORDS_FILE} is empty")
            return None
        
        # Return first line WITHOUT removing it
        return lines[0]
        
    except Exception as e:
        print(f"❌ Error reading keywords.txt: {e}")
        return None


def remove_keyword_from_file():
    """Remove the first line from keywords.txt after successful generation"""
    if not os.path.exists(KEYWORDS_FILE):
        print(f"❌ {KEYWORDS_FILE} not found")
        return False
    
    try:
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        
        if not lines:
            return False
        
        # Remove first line
        lines.pop(0)
        
        # Write remaining lines back
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        
        print(f"✅ Removed keyword from file")
        print(f"📊 Keywords remaining: {len(lines)}")
        return True
        
    except Exception as e:
        print(f"❌ Error removing keyword: {e}")
        return False


def get_keywords_count():
    """Get the number of keywords remaining"""
    if not os.path.exists(KEYWORDS_FILE):
        return 0
    
    try:
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        return len(lines)
    except:
        return 0