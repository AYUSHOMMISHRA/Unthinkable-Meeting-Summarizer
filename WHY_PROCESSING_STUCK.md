## Why Processing Gets Stuck on Railway 🔍

### Root Cause Analysis:

When you upload a file on Railway, here's what happens:

1. ✅ **File uploads successfully** (403 CSRF issue is fixed)
2. ✅ **Processing page opens** (shows "Processing...")
3. ❌ **Background thread starts** but...
4. ❌ **Transcription service tries to initialize**
5. ❌ **Raises ValueError: "API key not configured"** 
6. ❌ **Processing thread dies silently**
7. ❌ **Meeting status never updates from 'processing' to 'completed'**
8. ❌ **Page polls forever waiting for status change**

### The Exact Problem:

Your `meetings/services/transcription_service.py` requires either:
- `GROQ_API_KEY` (for FREE Whisper transcription), OR
- `OPENAI_API_KEY` (for OpenAI/OpenRouter transcription)

**If neither is set in Railway environment variables, the service raises:**
```python
raise ValueError("API key not configured. Set GROQ_API_KEY or OPENAI_API_KEY in settings.")
```

This exception is caught by the background thread, the meeting status is set to `'failed'`, but the processing page **keeps polling forever** because the JavaScript doesn't check for the 'failed' status.

---

## Immediate Solutions:

### Solution 1: Set Environment Variables in Railway (5 minutes)

**Go to Railway Dashboard:**

1. Open: https://railway.app/dashboard
2. Select your project: **Unthinkable-Meeting-Summarizer**
3. Click on your deployment
4. Go to **"Variables"** tab
5. Click **"+ New Variable"**
6. Add these variables:

```bash
# Required (choose one or both):
GROQ_API_KEY=gsk_your_groq_api_key_here

# OR

OPENAI_API_KEY=your_openai_api_key_here

# Recommended:
DEBUG=False
SECRET_KEY=your-super-secret-random-key-here
OPENAI_TIMEOUT=600
```

**Where to get FREE API keys:**

- **Groq (FREE Whisper)**: https://console.groq.com/keys
- **OpenRouter (Summarization)**: https://openrouter.ai/keys

7. Click **"Add"** for each variable
8. Railway will **automatically redeploy** (wait 1-2 minutes)
9. Try uploading again - it should work!

---

### Solution 2: Check Current Railway Logs (Right Now)

To see the exact error:

1. Go to Railway Dashboard
2. Click on your deployment
3. Go to **"Deployments"** tab
4. Click the latest deployment
5. Look for these errors in logs:
   - `ValueError: API key not configured`
   - `decouple.UndefinedValueError: GROQ_API_KEY not found`
   - `decouple.UndefinedValueError: OPENAI_API_KEY not found`

---

### Solution 3: Test Locally with API Keys

To verify everything works with API keys:

```bash
# Export API keys in your terminal
export GROQ_API_KEY="your_groq_key_here"
export OPENAI_API_KEY="your_openai_key_here"

# Restart the Django server
python manage.py runserver 0.0.0.0:8000

# Test upload - should process quickly
```

---

## Why It Works Fast Locally:

Your local `.env` file (not pushed to GitHub) likely has:
```
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=...
```

So locally, the services initialize successfully and processing completes.

On Railway, **these environment variables don't exist yet**, so processing fails immediately.

---

## Quick Test (After Setting Variables):

Once you add the variables to Railway and it redeploys:

1. Go to: https://unthinkable-meeting-summarizer-production.up.railway.app/
2. Upload a **small audio file** (< 1 minute)
3. Processing should complete in 10-30 seconds
4. You should see the results page

---

## Need Help?

If after setting the variables it still doesn't work:

1. Check Railway logs for errors
2. Visit: https://unthinkable-meeting-summarizer-production.up.railway.app/health/
   (After the latest deployment finishes)
3. This will show you exactly what's misconfigured

---

## TL;DR - The Fix:

**Railway → Your Project → Variables → Add:**
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
```

Wait 2 minutes for redeploy. Upload again. Should work! ✅
