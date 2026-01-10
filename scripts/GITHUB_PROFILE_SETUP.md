# 🔐 GSC Cookie-Based Authentication Setup

Complete guide to set up Google Search Console browser automation using cookies in GitHub Actions.

---

## 📋 Overview

This setup extracts only your Google authentication cookies (6.92 KB) instead of the full Chrome profile (22 MB), making it compatible with GitHub Secrets' 64 KB limit.

---

## 🚀 Step-by-Step Setup

### Step 1: First-Time Login (One-Time Setup)

Run the login script to save your Google authentication locally:

```bash
cd /Users/sushilmohan/Documents/ur-lawyer.github.io
python3 scripts/first_time_gsc_login.py
```

**What happens:**
- Chrome opens with Google Search Console
- You manually log in to your Google account
- Complete any 2FA if required
- Press ENTER when you see the GSC dashboard
- Profile saved to `~/.gsc_chrome_profile`

---

### Step 2: Extract Cookies

After successful login, extract only the cookies:

```bash
python3 scripts/extract_cookies.py
```

**Output:**
```
✅ Extracted 30 Google cookies
📊 Cookie data size: 5.19 KB
📊 Encoded size: 6.92 KB
💾 Saved to: gsc_cookies_encoded.txt
```

---

### Step 3: Copy Cookies to Clipboard

```bash
cat gsc_cookies_encoded.txt | pbcopy
echo "✅ Cookies copied!"
```

---

### Step 4: Add to GitHub Secrets

1. Open: https://github.com/ur-lawyer/ur-lawyer.github.io/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name**: `GSC_COOKIES`
4. **Value**: Press `Cmd+V` to paste
5. Click **"Add secret"**

---

### Step 5: Clean Up Sensitive Files

```bash
rm gsc_cookies_encoded.txt
rm -f chrome_profile_encoded.txt  # if exists
```

⚠️ **Important**: These files contain your Google credentials!

---

### Step 6: Deploy to GitHub

```bash
git add .
git commit -m "Update GSC automation with cookie-based auth"
git push origin master
```

---

## ✅ Verification

After pushing, check GitHub Actions logs for:

```
✅ Loaded 30 cookies from environment
✅ Cookies loaded into browser
🔍 Submitting URL to Google Search Console
✅ URL submitted to Google Search Console!
```

---

## 🔄 Updating Cookies

If authentication expires or you need to re-login:

```bash
# Step 1: Re-login
python3 scripts/first_time_gsc_login.py

# Step 2: Extract new cookies
python3 scripts/extract_cookies.py

# Step 3: Copy to clipboard
cat gsc_cookies_encoded.txt | pbcopy

# Step 4: Update GitHub Secret
# Go to GitHub → Settings → Secrets → GSC_COOKIES → Update

# Step 5: Clean up
rm gsc_cookies_encoded.txt
```

---

## ⚙️ How It Works

**Local Development:**
- Uses saved Chrome profile from `~/.gsc_chrome_profile`
- No changes needed

**GitHub Actions:**
1. Reads `GSC_COOKIES` from GitHub Secrets
2. Decodes base64-encoded cookies
3. Injects cookies into Chrome session
4. Browser authenticated automatically
5. Submits URLs to GSC

---

## 📊 Size Comparison

| Method | Size | GitHub Secrets Compatible |
|--------|------|--------------------------|
| Full Profile | 22.29 MB | ❌ No (357x too large) |
| **Cookies Only** | **6.92 KB** | ✅ **Yes!** |

**Reduction: 99.97%** 🎉

---

## 🛠️ Troubleshooting

**"Cookies database not found"**
- Run `first_time_gsc_login.py` first to create the profile

**"GitHub Secret too large"**
- You're using the wrong file - use `gsc_cookies_encoded.txt`, not `chrome_profile_encoded.txt`

**"Authentication failed in GitHub Actions"**
- Cookies may have expired - re-run extraction steps above
- Update `GSC_COOKIES` secret with new value

**"No cookies loaded from environment"**
- Verify secret name is exactly: `GSC_COOKIES`
- Check the secret value was copied completely

---

## 🔒 Security Notes

✅ Only authentication cookies are extracted (not entire profile)  
✅ Cookies are base64-encoded in GitHub Secrets  
✅ Never exposed in GitHub Actions logs  
✅ Accessible only to this repository  
⚠️ Repository collaborators can access secrets
