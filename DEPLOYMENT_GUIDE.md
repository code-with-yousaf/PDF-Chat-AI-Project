# 🚀 Deployment Guide - API Key Setup

## Problem: API Key Not Working on Streamlit Cloud

### ✅ Solution: Use Free Groq API (Recommended)

Groq is **100% free** with 14,400 requests/day and works perfectly!

---

## Step-by-Step Setup

### 1. Get Free Groq API Key (2 minutes)

1. Open: **https://console.groq.com**
2. Click **"Sign in"** (top right)
3. Choose **"Continue with Google"** (or GitHub/Email)
4. After login, click **"API Keys"** (left sidebar)
5. Click **"Create API Key"** button
6. Copy the key (starts with `gsk_...`)

---

### 2. Add to Streamlit Cloud

1. Go to: **https://share.streamlit.io/**
2. Find your app: **"PDF-Chat-AI-Project"**
3. Click the **"⋮"** (three dots) → **Settings**
4. Click **"Secrets"** tab (left side)
5. **DELETE any old secrets** in the box
6. Paste **exactly this** (replace with your key):

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

7. Click **"Save"** (bottom right)
8. App will **reboot automatically** (wait 1-2 minutes)

---

### 3. Test

1. Open your app
2. Type: "Hello"
3. You should get a **real AI response** from Llama 3.1!

---

## ⚠️ Common Mistakes

❌ **Wrong:**
```toml
GROQ_API_KEY = gsk_xxx  (missing quotes)
GROQ_API_KEY: "gsk_xxx"  (using colon instead of =)
"GROQ_API_KEY" = "gsk_xxx"  (quotes around key name)
```

✅ **Correct:**
```toml
GROQ_API_KEY = "gsk_your_key_here"
```

---

## 🔑 Alternative: OpenAI API

If you have OpenAI credits:

```toml
OPENAI_API_KEY = "sk-proj-your_key_here"
```

**Note:** OpenAI is paid ($5 minimum deposit required)

---

## 🆓 Why Groq?

- ✅ **100% Free** (14,400 requests daily)
- ✅ **Super Fast** (fastest inference)
- ✅ **Easy Setup** (1-click Google login)
- ✅ **Good Quality** (Llama 3.1 70B model)
- ✅ **No Credit Card** needed

---

## 🐛 Still Not Working?

**Check these:**

1. **Secrets saved?** Make sure you clicked "Save" button
2. **App rebooted?** Wait 2 minutes after saving
3. **Key correct?** Copy-paste again (no extra spaces)
4. **Quotes correct?** Use straight quotes `"` not curly `""`

**Get exact error:**
- Chat with the app
- Screenshot the error message
- Share for debugging

---

## 📞 Need Help?

- Check app logs: Streamlit Cloud → Your App → "Manage app" → "Logs"
- Error will show exact issue

---

**Last Updated:** December 2024
