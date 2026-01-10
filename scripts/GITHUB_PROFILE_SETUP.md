# 🔐 GitHub Secrets Chrome Profile Setup Guide

## 📋 Overview

This guide shows you how to store your Chrome profile in GitHub Secrets so browser automation works in GitHub Actions.

---

## 🚀 Step-by-Step Instructions

### Step 1: Encrypt Your Chrome Profile

Run the encryption script locally:

```bash
cd /Users/sushilmohan/Documents/ur-lawyer.github.io
python3 scripts/encrypt_profile.py
```

**Output:**
- Creates `chrome_profile_encoded.txt` with your encrypted profile
- Shows compression statistics

---

### Step 2: Copy the Encoded Profile

```bash
# Copy to clipboard (macOS)
cat chrome_profile_encoded.txt | pbcopy

# Or manually open and copy:
open chrome_profile_encoded.txt
```

---

### Step 3: Add to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GSC_CHROME_PROFILE`
5. Value: Paste the encoded profile
6. Click **Add secret**

---

### Step 4: Delete the Local File

**IMPORTANT**: Delete the encoded file (contains credentials):

```bash
rm chrome_profile_encoded.txt
```

---

### Step 5: Test in GitHub Actions

Commit and push your changes:

```bash
git add .
git commit -m "Add encrypted Chrome profile support"
git push origin master
```

Watch the workflow - it should now restore your profile and use it for GSC automation!

---

## ✅ How It Works

1. **Workflow starts** → Decodes `GSC_CHROME_PROFILE` secret
2. **Extracts to** → `~/.gsc_chrome_profile`
3. **Browser uses** → Saved authentication
4. **Workflow ends** → Profile deleted automatically

---

## 🔒 Security Notes

- ✅ Encrypted in GitHub Secrets
- ✅ Never exposed in logs
- ✅ Auto-deleted after each run
- ✅ Only accessible to this repository
- ⚠️ Repository collaborators can access secrets

---

## 🔄 Updating the Profile

If you need to re-login or update your profile:

1. Run `python3 scripts/first_time_gsc_login.py` locally
2. Run `python3 scripts/encrypt_profile.py` again
3. Update the `GSC_CHROME_PROFILE` secret in GitHub
4. Done!

---

## ⚠️ Troubleshooting

**Profile not restored in GitHub Actions?**
- Check secret name is exactly: `GSC_CHROME_PROFILE`
- Verify secret value was copied completely
- Check workflow logs for "Restoring Chrome profile" step

**Authentication fails in GitHub Actions?**
- Profile may have expired (Google sessions expire)
- Re-run steps above to update profile
- Google may block automated sessions (rate limiting)

---

## 🎯 Next Steps

After setup is complete, your workflow will:
- ✅ Generate blog posts automatically
- ✅ Submit URLs to GSC using browser automation
- ✅ Work exactly like your local setup
- ✅ No manual intervention needed!
