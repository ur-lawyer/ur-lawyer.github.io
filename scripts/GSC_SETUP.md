# Google Search Console Automation - Quick Start Guide

## 🚀 Quick Start

### 1️⃣ First-Time Setup (Run Locally Once)

```bash
cd /Users/sushilmohan/Documents/ur-lawyer.github.io/scripts
pip install selenium
python3 first_time_gsc_login.py
```

**Follow the prompts:**
- Chrome will open
- Log in to your Google account
- Press ENTER when logged in
- Session saved to `~/.gsc_chrome_profile`

### 2️⃣ Test Locally (Optional)

```bash
# Test with visible browser
python3 gsc_automation.py --url "https://ur-lawyer.github.io" --visible
```

### 3️⃣ Deploy to GitHub

```bash
git add .
git commit -m "Add GSC automation"
git push origin master
```

---

## 📝 How It Works

When GitHub Actions generates a new post:

1. **Post created** → `post_url` = "https://ur-lawyer.github.io/new-post"
2. **URLS_TO_SUBMIT** = `post_url` (as you requested)
3. **API indexing** → Submits via Google Indexing API
4. **Browser indexing** → Submits via `submit_url_to_gsc(URLS_TO_SUBMIT)`
5. **Combined status logged** → "API: Success | GSC: Success (Browser)"

---

## 🔧 Configuration

All settings in [`config.py`](file:///Users/sushilmohan/Documents/ur-lawyer.github.io/scripts/config.py):

```python
GSC_PROPERTY_URL = "https://ur-lawyer.github.io"  # Your site
GSC_CHROME_PROFILE_PATH = "~/.gsc_chrome_profile"  # Profile location
GSC_HEADLESS = True                                  # Headless in CI/CD
```

---

## 🎯 Files Created/Modified

### New Files:
- `scripts/first_time_gsc_login.py` - One-time authentication
- `scripts/gsc_automation.py` - URL submission automation

### Modified Files:
- `scripts/config.py` - Added GSC settings
- `scripts/generate_posts.py` - Integrated GSC automation
- `.github/workflows/auto-blog.yml` - Added Selenium/Chrome

---

## 💡 Usage Examples

### Submit Single URL
```bash
python3 gsc_automation.py --url "https://ur-lawyer.github.io/my-post"
```

### Submit Multiple URLs
```bash
python3 gsc_automation.py --urls \
  "https://ur-lawyer.github.io/post1" \
  "https://ur-lawyer.github.io/post2"
```

### Clean Up Profile
```bash
python3 gsc_automation.py --cleanup
```

---

## ✅ What You Requested - Implemented

✅ **Use `gsc_automation.py`** - Created with Selenium logic  
✅ **First-time login with `first_time_gsc_login.py`** - Interactive authentication  
✅ **`URLS_TO_SUBMIT` variable** - Holds current generated post URL  
✅ **Chrome profile cleanup** - Deleted after GitHub Actions caches login  
✅ **Same logic pattern** - Follows your Twitter/LinkedIn posting pattern

---

## 🔐 Security

- Chrome profile created locally for first-time auth
- Profile deleted after each GitHub Actions run
- No credentials stored in GitHub
- Headless mode in CI/CD

---

## 📊 Next Steps

1. **Test locally:** Run `first_time_gsc_login.py` to authenticate
2. **Commit changes:** Push to GitHub to activate automation
3. **Monitor:** Check GitHub Actions logs for indexing status

Your blog posts will now be automatically submitted to Google Search Console! 🎉
