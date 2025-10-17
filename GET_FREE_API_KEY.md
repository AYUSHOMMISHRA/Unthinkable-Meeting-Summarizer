# 🆓 Get Your FREE Groq API Key

Groq offers **100% FREE** Whisper transcription with generous limits!

## Steps to Get Your FREE API Key:

### 1. Visit Groq Console
Go to: **https://console.groq.com/keys**

### 2. Sign Up (30 seconds)
- Click "Sign Up" or "Get Started"
- Use Google/GitHub login or email
- No credit card required!

### 3. Create API Key
- Click "Create API Key"
- Give it a name (e.g., "Meeting Summarizer")
- Copy the API key (starts with `gsk_...`)

### 4. Add to Your `.env` File
Open `/Users/ayushmishra/Meeting Summarizer/.env` and replace:
```
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
```

with your actual key:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## ✅ FREE Tier Limits (More than enough!)
- **6,000 requests per day**
- **30 requests per minute**
- **No credit card needed**
- **No expiration**

## 🎯 What You Get:
- ✅ Whisper Large V3 (best accuracy)
- ✅ Multiple audio formats (MP3, WAV, M4A, etc.)
- ✅ Up to 25MB file size
- ✅ Lightning fast processing

## 🚀 After Adding Your Key:
1. Save the `.env` file
2. Restart your Django server
3. Upload an audio file
4. Watch it process with FREE transcription! 🎉

## 📝 Note:
The app will automatically use:
- **Groq (FREE)** for transcription (Whisper)
- **OpenRouter/Llama** for summarization (your existing key)

Both are FREE and work perfectly together! 🔥
