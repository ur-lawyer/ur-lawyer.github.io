# Social Media Auto-Posting Setup Guide

This guide shows you how to set up automatic posting to Twitter and LinkedIn.

## 📋 New Keywords.txt Format

Your keywords.txt now supports 7 columns (separated by `|`):

```
title | focus_keyword | permalink | semantic_keyword | affiliate_links | linkedin_content | twitter_content
```

### Example:

```
How to Build AI Agents | ai agents tutorial | /ai-agents-tutorial/ | LangGraph, LangChain, OpenAI | Udemy course: https://... | 🚀 Just spent 40 hours learning LangGraph... [full LinkedIn post] | 🧵 How to build your first agent (thread)... [full Twitter thread]
```

## 🐦 Twitter/X Setup

### Step 1: Create Twitter Developer Account

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Sign up for a developer account
3. Create a new App
4. Get your credentials

### Step 2: Get API Credentials

You need 5 credentials:

1. **API Key** (Consumer Key)
2. **API Secret** (Consumer Secret)
3. **Access Token**
4. **Access Token Secret**
5. **Bearer Token**

### Step 3: Add to GitHub Secrets

Go to Settings → Secrets → Actions → New secret:

| Secret Name | Value |
|-------------|-------|
| `TWITTER_API_KEY` | Your API Key |
| `TWITTER_API_SECRET` | Your API Secret |
| `TWITTER_ACCESS_TOKEN` | Your Access Token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Your Access Token Secret |
| `TWITTER_BEARER_TOKEN` | Your Bearer Token |
| `TWITTER_USERNAME` | Your Twitter handle (e.g., `yourusername`) |

### Twitter Post Features:

✅ Supports single tweets
✅ Supports Twitter threads (automatically splits)
✅ Replaces `[link]` with actual post URL
✅ Adds affiliate links at the end
✅ Handles 280 character limit

## 💼 LinkedIn Setup

### Step 1: Create LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Request access to the Marketing Developer Platform
4. Get OAuth 2.0 credentials

### Step 2: Get Access Token

LinkedIn uses OAuth 2.0, so you need to:

1. Get authorization code
2. Exchange for access token
3. Use access token in API calls

**Note:** LinkedIn access tokens expire after 60 days, so you'll need to refresh them.

### Step 3: Get Your Person ID

Run this API call to get your LinkedIn Person ID:

```bash
curl -X GET 'https://api.linkedin.com/v2/me' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Look for the `id` field in the response.

### Step 4: Add to GitHub Secrets

| Secret Name | Value |
|-------------|-------|
| `LINKEDIN_ACCESS_TOKEN` | Your OAuth access token |
| `LINKEDIN_PERSON_ID` | Your person ID (from step 3) |

### LinkedIn Post Features:

✅ Posts with article link preview
✅ Supports up to 3000 characters
✅ Replaces `[link]` with actual post URL
✅ Adds affiliate links
✅ Supports hashtags and emojis

## 📝 Keywords.txt Examples

### Old Format (Still Works):

```
Personal Injury Lawyer Guide | personal injury | /personal-injury-guide/ | legal advice
```

### New Format with Social Media:

```
Personal Injury Lawyer Guide | personal injury | /personal-injury-guide/ | legal advice | Get 20% off LegalZoom: https://... | 💼 After 10 years as a personal injury lawyer, here's what I wish clients knew before hiring... [Full LinkedIn post with insights] | 🧵 Thread: What to do immediately after an accident (10 tweets) [1/10] First 24 hours are crucial... [2/10] Document everything...
```

## 🎯 Writing Effective Social Media Content

### LinkedIn Tips:

- Start with a hook (🚀 emoji + attention grabber)
- Use numbered lists (1), 2), 3))
- Include personal experience
- Add relevant hashtags at the end
- Keep under 3000 characters
- End with a call-to-action

### Twitter Thread Tips:

- Mark tweets with [1/10], [2/10], etc.
- Keep each tweet under 280 characters
- Use emojis strategically
- Include code snippets as images
- End with a link to full article
- Use "Bookmark this thread 🔖"

## 🔄 Workflow Process

When a post is published:

1. ✅ Generate blog article
2. ✅ Generate image
3. ✅ Save to _posts/
4. ✅ Wait 3 minutes for deployment
5. ✅ Submit to Google Search Console
6. ✅ Log to Google Sheets
7. ✅ **Post to Twitter** (if content provided)
8. ✅ **Post to LinkedIn** (if content provided)
9. ✅ Remove keyword from file
10. ✅ Commit changes

## ⚠️ Important Notes

### Twitter:

- Free tier: 1,500 tweets per month
- API v2 required
- Threads post with 2-second delays between tweets

### LinkedIn:

- Access tokens expire after 60 days
- Need to refresh tokens regularly
- Posts appear immediately
- Article previews are generated automatically

## 🧪 Testing

### Test Twitter Posting:

```python
python -c "from twitter_poster import post_to_twitter; post_to_twitter('Test', '/test/', 'This is a test tweet with [link]')"
```

### Test LinkedIn Posting:

```python
python -c "from linkedin_poster import post_to_linkedin; post_to_linkedin('Test', '/test/', 'This is a test LinkedIn post with [link]')"
```

## 📊 What Gets Posted

Each successful blog post will:

- 📝 Create blog article on your site
- 🖼️ Generate featured image
- 🐦 Post to Twitter (with thread if provided)
- 💼 Post to LinkedIn (with article preview)
- 📊 Log everything to Google Sheets
- 🔍 Submit to Google for indexing

## 🚫 Optional Features

If you don't want social media posting:

- Simply leave the `linkedin_content` and `twitter_content` columns empty
- The script will skip posting to those platforms
- Everything else continues to work normally

Example (no social media):

```
Title | keyword | permalink | semantic | | |
```

The last two `|` leave the social media fields empty.