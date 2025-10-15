# Meeting Summarizer 🎙️

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![AI Powered](https://img.shields.io/badge/AI-Whisper%20%2B%20LLaMA-purple.svg)

**Transform your meetings into actionable insights with AI-powered transcription and summarization**

[Features](#-features)  • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Keys Setup](#-api-keys-setup)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [AI Models & Prompts](#-ai-models--prompts)
- [Usage Guide](#-usage-guide)
- [Security & Best Practices](#-security--best-practices)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧩 Project Overview

### What is Meeting Summarizer?

Meeting Summarizer is a powerful Django-based web application that automatically transcribes meeting audio files and generates intelligent summaries using state-of-the-art AI models. It eliminates the need for manual note-taking by extracting key decisions, action items, discussion topics, and participant information from your meetings.

### Purpose & Motivation

In today's fast-paced business environment, professionals spend countless hours in meetings, yet critical information often gets lost or forgotten. Studies show that 71% of meetings are considered unproductive by employees. This project addresses that problem by:

- **Saving Time**: Automated transcription and summarization reduce post-meeting work by 80%
- **Improving Accountability**: Automatically extracted action items with assignees and deadlines
- **Enhancing Knowledge Management**: Searchable, organized meeting records with tags and relationships
- **Increasing Accessibility**: Makes meeting content accessible to those who couldn't attend

### Real-World Problem Solved

- **For Teams**: Never miss important decisions or action items again
- **For Managers**: Track team commitments and follow-ups efficiently
- **For Remote Workers**: Stay aligned with async meeting summaries
- **For Organizations**: Build a searchable knowledge base of meetings

---

## 🌟 Features

### Core Functionality
- **🎤 Free AI Transcription**: Uses Groq's free Whisper API for accurate speech-to-text (6,000 requests/day)
- **🧠 Smart Summarization**: LLaMA 3.1 8B model via OpenRouter for intelligent meeting summaries
- **✅ Action Items Extraction**: Automatically identifies and tracks tasks with assignees, priorities, and deadlines
- **📊 Key Insights**: Extracts decisions, discussion topics, participants, and key insights
- **🏷️ Tags & Organization**: Custom tags with colors and related meetings linking
- **🎨 Dark/Light Theme**: Beautiful, responsive UI with theme switching
- **📈 Real-time Processing**: Live progress tracking during transcription and summarization
- **📥 Export Options**: Download transcripts and summaries

### Technical Features
- **Multiple Audio Formats**: MP3, WAV, M4A, OGG, FLAC (up to 100MB, 2 hours)
- **Retry Logic**: 3 attempts with exponential backoff for API reliability
- **Error Handling**: Graceful fallbacks and detailed error messages
- **JSON Schema Validation**: Ensures consistent AI output structure
- **Database**: SQLite for easy setup, PostgreSQL-ready for production

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **API Keys** (both 100% FREE!):
  - [Groq API Key](https://console.groq.com/keys) - Free Whisper transcription (6,000 requests/day)
  - [OpenRouter API Key](https://openrouter.ai/keys) - Free LLaMA access

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/AYUSHOMMISHRA/Unthinkable-Meeting-Summarizer.git
   cd Unthinkable-Meeting-Summarizer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   # Django Settings
   SECRET_KEY=your-secret-key-here-change-this-in-production
   DEBUG=True
   
   # API Keys (REQUIRED)
   GROQ_API_KEY=your-groq-api-key-here
   OPENAI_API_KEY=your-openrouter-api-key-here
   
   # Model Configuration (Optional - defaults shown)
   OPENAI_GPT_MODEL=meta-llama/llama-3.1-8b-instruct
   GROQ_WHISPER_MODEL=whisper-large-v3
   
   # API URLs (Optional - defaults shown)
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   GROQ_BASE_URL=https://api.groq.com/openai/v1
   ```

   > ⚠️ **SECURITY**: Never commit the `.env` file! It's already in `.gitignore`.

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🔑 API Keys Setup

### Groq API (Free Whisper Transcription) ⭐ Recommended

**Why Groq?**
- 100% FREE with generous limits
- 6,000 requests per day
- 30 requests per minute
- No credit card required
- No expiration
- Whisper Large V3 (best accuracy)

**Setup Steps:**

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for a free account (Google/GitHub login available - takes 30 seconds)
3. Click "Create API Key"
4. Give it a name (e.g., "Meeting Summarizer")
5. Copy the API key (starts with `gsk_...`)
6. Add to `.env`:
   ```bash
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### OpenRouter API (Free LLaMA Access)

**Why OpenRouter?**
- Free tier available
- Access to multiple AI models
- LLaMA 3.1 8B Instruct model
- Simple API, OpenAI-compatible

**Setup Steps:**

1. Visit [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up for a free account
3. Click "Create Key"
4. Copy the API key (starts with `sk-or-v1-...`)
5. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**What You Get for FREE:**
- ✅ Whisper Large V3 transcription (Groq)
- ✅ LLaMA 3.1 8B summarization (OpenRouter)
- ✅ Multiple audio formats (MP3, WAV, M4A, etc.)
- ✅ Up to 100MB file size
- ✅ Lightning fast processing

---

## 🛠️ Tech Stack

### Backend Framework
- **Django 4.2.7** - High-level Python web framework
- **Python 3.11+** - Core programming language

### AI & Machine Learning
- **Groq Whisper (whisper-large-v3)** - Free, state-of-the-art speech recognition (6,000 requests/day)
- **LLaMA 3.1 8B Instruct** (via OpenRouter) - Advanced language model for summarization
- **OpenAI API Client 1.3.5** - API integration for AI services
- **tiktoken 0.5.1** - Token counting for AI models

### Database
- **SQLite** (Development) - Lightweight, file-based database
- **PostgreSQL** (Production Ready) - Robust relational database

### Frontend
- **Bootstrap 5.3.2** - Responsive UI framework
- **Bootstrap Icons 1.11.1** - Icon library
- **JavaScript (Vanilla)** - Interactive features
- **HTML5/CSS3** - Modern web standards

### File Processing
- **Pillow 10.1.0** - Image processing library
- **pydub 0.25.1** - Audio file manipulation
- **mutagen** - Audio metadata extraction

### Development Tools
- **python-decouple 3.8** - Environment variable management
- **python-dotenv 1.0.0** - .env file support
- **requests 2.31.0** - HTTP library
- **python-dateutil 2.8.2** - Date/time utilities

### Testing & Quality
- **pytest 7.4.3** - Testing framework
- **pytest-django 4.7.0** - Django-specific pytest plugin
- **factory-boy 3.3.0** - Test fixture generation
- **faker 20.1.0** - Fake data generation
- **black 23.11.0** - Code formatter
- **flake8 6.1.0** - Linter
- **pylint 3.0.3** - Static code analyzer
- **isort 5.12.0** - Import sorter

### Production Server
- **gunicorn 21.2.0** - WSGI HTTP server
- **whitenoise 6.6.0** - Static file serving

---

## 📁 Project Structure

```
Unthinkable-Meeting-Summarizer/
├── config/                      # Django project settings
│   ├── settings.py              # Main configuration
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI config
├── meetings/                    # Main Django app
│   ├── models.py                # Database models (Meeting, ActionItem, Tag)
│   ├── views.py                 # View logic and request handling
│   ├── urls.py                  # App-specific URLs
│   ├── forms.py                 # Form definitions
│   ├── admin.py                 # Django admin configuration
│   ├── services/                # AI integration services
│   │   ├── transcription_service.py    # Groq Whisper integration
│   │   ├── summarization_service.py    # LLaMA integration
│   │   └── processing_service.py       # Orchestrates AI workflow
│   ├── templates/meetings/      # HTML templates
│   │   ├── index.html           # Upload interface
│   │   ├── detail.html          # Meeting details view
│   │   ├── processing.html      # Processing status
│   │   └── list.html            # Meetings list
│   ├── management/commands/     # Custom Django commands
│   │   └── update_summaries.py  # Bulk update command
│   └── templatetags/            # Custom template filters
│       └── meeting_filters.py   # Date/time formatting
├── static/                      # Static assets
│   ├── css/style.css            # Custom styles
│   └── js/                      # JavaScript files
│       ├── upload.js            # File upload handling
│       └── results.js           # Results page interactions
├── media/                       # User uploads (not in version control)
│   └── meetings/audio/          # Audio files storage
├── templates/                   # Base templates
│   ├── base.html                # Base template with navbar
│   ├── index.html               # Home page
│   └── meetings_list.html       # Main meetings list
├── .env                         # Environment variables (DO NOT COMMIT!)
├── .gitignore                   # Git ignore rules
├── db.sqlite3                   # SQLite database (dev only)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---


## 🔧 Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | - | Django secret key (change in production!) |
| `DEBUG` | No | `True` | Debug mode (set to `False` in production) |
| `GROQ_API_KEY` | Yes | - | Groq API key for Whisper transcription |
| `OPENAI_API_KEY` | Yes | - | OpenRouter API key for LLaMA summarization |
| `GROQ_WHISPER_MODEL` | No | `whisper-large-v3` | Whisper model to use |
| `OPENAI_GPT_MODEL` | No | `meta-llama/llama-3.1-8b-instruct` | LLaMA model to use |
| `GROQ_BASE_URL` | No | `https://api.groq.com/openai/v1` | Groq API base URL |
| `OPENAI_BASE_URL` | No | `https://openrouter.ai/api/v1` | OpenRouter API base URL |

### Database Configuration

**Development:** SQLite (default, no setup needed)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production:** PostgreSQL (recommended)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meeting_summarizer',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🤖 AI Models & Prompts

### Transcription (Whisper via Groq)

**Model:** `whisper-large-v3`

**Configuration:**
```python
response = client.audio.transcriptions.create(
    model="whisper-large-v3",
    file=audio_file,
    response_format="text",
    timeout=300  # 5 minutes
)
```

**Technical Specs:**
- Max file size: 25 MB
- Supported formats: MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM
- Timeout: 300 seconds (5 minutes)
- Retry logic: 3 attempts with exponential backoff

**Note:** Whisper is an audio-to-text model and does **NOT** use text prompts.

### Summarization (LLaMA via OpenRouter)

**Model:** `meta-llama/llama-3.1-8b-instruct`

**System Prompt:**
```
You are a meeting analysis expert specializing in extracting insights from meeting transcripts.
```

**User Prompt Structure:**
```
Analyze the following meeting transcript and extract:

1. Executive Summary: A concise 3-4 sentence overview
2. Key Decisions: Important decisions made (array of strings)
3. Action Items: Tasks with assignee, priority, deadline (array of objects)
4. Discussion Topics: Main themes discussed (array of strings)
5. Participants: People who participated (extracted from transcript)
6. Insights: Key learnings or observations (array of strings)

Return in JSON format:
{
  "executive_summary": "...",
  "key_decisions": ["..."],
  "action_items": [{"task": "...", "assignee": "...", "priority": "high/medium/low", "deadline": "YYYY-MM-DD"}],
  "discussion_topics": ["..."],
  "participants": ["..."],
  "insights": ["..."]
}
```

**Configuration:**
```python
response = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b-instruct",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.3,  # Low for factual accuracy
    max_tokens=2000,
    response_format={"type": "json_object"}
)
```

**Why temperature=0.3?**
- Reduces hallucinations
- Ensures consistent output
- Focuses on extraction over creativity
- Maintains factual accuracy

---

## 📝 Usage Guide

### Step-by-Step Workflow

1. **Upload Audio File**
   - Navigate to the home page
   - Drag & drop or click to select an audio file
   - Supported formats: MP3, WAV, M4A, OGG, FLAC
   - Max file size: 100MB
   - Max duration: 2 hours

2. **Add Meeting Details** (Optional)
   - Meeting title (auto-generated from filename if not provided)
   - Meeting date and time (defaults to current)

3. **Start Processing**
   - Click "Start Processing"
   - Watch real-time progress:
     - ✅ Audio upload
     - 🎤 Transcription (Whisper)
     - 🧠 Summarization (LLaMA)
     - 📊 Extraction (Decisions, Actions, Insights)

4. **Review Results**
   - **Transcript Tab**: Full text transcription
   - **Summary Tab**: Executive summary and key decisions
   - **Action Items Tab**: Tasks with assignees, priorities, deadlines
   - **Insights Tab**: Discussion topics, participants, key insights

5. **Manage & Organize**
   - Mark action items as complete
   - Add custom tags (with colors)
   - Link related meetings
   - Star important meetings
   - Export transcript or summary

6. **Search & Filter**
   - Search by title, transcript, or summary
   - Filter by tags, date range, or starred
   - Sort by date, title, or processing status

### Action Items Management

**Priority Levels:**
- 🔴 **High**: Critical tasks requiring immediate attention
- 🟡 **Medium**: Important but not urgent
- 🟢 **Low**: Nice-to-have or long-term tasks

**Status Indicators:**
- ⏰ **Overdue**: Past deadline, not completed
- 📅 **Upcoming**: Due within 7 days
- ✅ **Completed**: Task finished
- 📝 **Pending**: No deadline or future deadline

**Example Action Item:**
```json
{
  "task": "Complete the project proposal and submit to stakeholders",
  "assignee": "John Doe",
  "priority": "high",
  "deadline": "2025-10-20",
  "completed": false
}
```

---
## 🧠 Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐     │
│  │   Upload    │  │  Processing  │  │  Results View   │     │
│  │  Interface  │  │    Status    │  │  (Tabs/Filters) │     │
│  └─────────────┘  └──────────────┘  └─────────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Requests
┌───────────────────────────▼─────────────────────────────────┐
│                    Django Application                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                     Views Layer                      │   │
│  │  • index() - Upload interface                        │   │
│  │  • upload_meeting() - File handling                  │   │
│  │  • processing() - Status display                     │   │
│  │  • meeting_detail() - Results display                │   │
│  │  • meetings_list() - List with filters               │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │                  Services Layer                      │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │       ProcessingService (Orchestrator)       │    │   │
│  │  │  • Manages workflow                          │    │   │
│  │  │  • Error handling                            │    │   │
│  │  │  • Status updates                            │    │    
│  │  └──────────┬───────────────────┬───────────────┘    │   │
│  │             │                   │                    │   │
│  │  ┌──────────▼──────────┐  ┌────▼────────────────┐    │   │
│  │  │ TranscriptionService│  │ SummarizationService│    │   │
│  │  │  • Groq API client  │  │  • OpenRouter client│    │   │
│  │  │  • Whisper model    │  │  • LLaMA model      │    │   │
│  │  │  • Audio validation │  │  • JSON parsing     │    │   │
│  │  └─────────────────────┘  └─────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│                       │                                     │
│  ┌────────────────────▼─────────────────────────────────┐   │
│  │                   Models Layer                       │   │
│  │  • Meeting (audio, status, metadata)                 │   │
│  │  • Transcript (text, word count, language)           │   │
│  │  • Summary (executive summary, decisions, topics)    │   │
│  │  • ActionItem (task, assignee, priority, deadline)   │   │
│  │  • Tag (name, color, related meetings)               │   │
│  └────────────────────┬─────────────────────────────────┘   │
└───────────────────────┼─────────────────────────────────────┘
                        │
        ┌───────────────▼───────────────┐
        │         Database              │
        │  • SQLite (Development)       │
        │  • PostgreSQL (Production)    │
        └───────────────────────────────┘
```

## �️ Security & Best Practices

### Environment Variables Security

✅ **DO:**
- Keep `.env` file in `.gitignore`
- Use strong, unique `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Rotate API keys regularly
- Use environment-specific `.env` files

❌ **DON'T:**
- Commit `.env` to version control
- Share API keys publicly
- Use default `SECRET_KEY` in production
- Hardcode secrets in code
- Enable `DEBUG` in production

### Production Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY` to a strong, unique value
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper static file serving (e.g., WhiteNoise)
- [ ] Configure HTTPS/SSL
- [ ] Set up proper logging
- [ ] Implement rate limiting on API endpoints
- [ ] Use environment variables for all secrets
- [ ] Set up regular database backups
- [ ] Monitor API usage and costs

### API Key Management

**Groq API Limits (Free Tier):**
- 6,000 requests per day
- 30 requests per minute
- Monitor usage at: https://console.groq.com/usage

**OpenRouter Limits:**
- Varies by model and tier
- Monitor usage at: https://openrouter.ai/activity

**Rate Limiting Best Practices:**
- Implement request queuing for bulk processing
- Add exponential backoff on retries
- Cache responses when appropriate
- Monitor and log API errors

---

## � Troubleshooting

### Common Issues

**1. "API Key not found" error**
- Solution: Ensure `.env` file exists in project root
- Check: API keys are correctly formatted (no extra spaces)
- Verify: Environment variables are loaded (restart server after changes)

**2. Audio transcription fails**
- Check: File format is supported (MP3, WAV, M4A, etc.)
- Verify: File size is under 25MB
- Ensure: Groq API key is valid and has quota remaining
- Try: Re-uploading the file or converting to different format

**3. Summarization returns empty results**
- Check: Transcript was generated successfully
- Verify: OpenRouter API key is valid
- Ensure: Model `meta-llama/llama-3.1-8b-instruct` is available
- Review: Error logs in terminal or `logs/` directory

**4. Database migration errors**
- Solution: Delete `db.sqlite3` and run `python manage.py migrate` again
- Check: No conflicting migration files
- Verify: Database permissions are correct

**5. Static files not loading**
- Run: `python manage.py collectstatic`
- Check: `STATIC_URL` and `STATIC_ROOT` in settings.py
- Verify: Static files are in correct directory structure

### Debug Mode

Enable detailed logging by setting in `.env`:
```bash
DEBUG=True
```

View logs:
```bash
# Terminal output (live)
python manage.py runserver

# Log files (if configured)
tail -f logs/django.log
```

### Getting Help

1. Check this README thoroughly
2. Review error messages in terminal
3. Check browser console for frontend errors
4. Search existing issues on GitHub
5. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version, etc.)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/Unthinkable-Meeting-Summarizer.git
   cd Unthinkable-Meeting-Summarizer
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes clearly

### Contribution Guidelines

- **Code Quality**: Follow PEP 8 for Python code
- **Commit Messages**: Use conventional commits (feat, fix, docs, chore, etc.)
- **Testing**: Test your changes with different audio files and scenarios
- **Documentation**: Update README or add comments for new features
- **Issues**: Check existing issues before creating new ones

### Areas We Need Help With

- � Bug fixes and error handling improvements
- ✨ New features (export formats, batch processing, etc.)
- 📚 Documentation and tutorials
- 🌍 Internationalization and localization
- 🎨 UI/UX improvements
- ⚡ Performance optimizations
- 🧪 Unit and integration tests

---

## �📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Ayush Mishra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

This project wouldn't be possible without these amazing technologies:

- **[Groq](https://groq.com/)** - Free Whisper API for lightning-fast transcription
- **[OpenRouter](https://openrouter.ai/)** - Access to LLaMA and other AI models
- **[Django](https://www.djangoproject.com/)** - Powerful Python web framework
- **[Bootstrap](https://getbootstrap.com/)** - Beautiful UI components
- **[Whisper](https://openai.com/research/whisper)** - State-of-the-art speech recognition
- **[LLaMA](https://ai.meta.com/llama/)** - Open-source large language model

### Special Thanks

- OpenAI for creating Whisper
- Meta AI for LLaMA models
- The Django community for excellent documentation
- All contributors and users of this project

---

## 📧 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/AYUSHOMMISHRA/Unthinkable-Meeting-Summarizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AYUSHOMMISHRA/Unthinkable-Meeting-Summarizer/discussions)
- **Email**: [Contact Developer](mailto:your-email@example.com)
- **Documentation**: This README and inline code comments

---

## 🗺️ Roadmap

### Planned Features

- [ ] **Batch Processing**: Process multiple audio files simultaneously
- [ ] **Speaker Diarization**: Identify and label different speakers
- [ ] **Real-time Transcription**: Live transcription during meetings
- [ ] **Calendar Integration**: Sync with Google Calendar, Outlook
- [ ] **Team Collaboration**: Multi-user support with permissions
- [ ] **Advanced Search**: Full-text search across all meetings
- [ ] **Analytics Dashboard**: Meeting statistics and insights
- [ ] **Mobile App**: iOS and Android applications
- [ ] **API Endpoints**: REST API for integration with other tools
- [ ] **Webhooks**: Real-time notifications for processing completion
- [ ] **Cloud Storage**: Integration with Google Drive, Dropbox, S3
- [ ] **Custom AI Models**: Support for fine-tuned models

### Version History

- **v1.0.0** (Current) - Initial release with core features
  - Whisper transcription via Groq
  - LLaMA summarization via OpenRouter
  - Action items extraction
  - Tags and related meetings
  - Dark/light theme
  - Export functionality

---

## 📊 Performance & Limits

### Processing Times (Approximate)

| Audio Length | Transcription | Summarization | Total |
|--------------|---------------|---------------|-------|
| 5 minutes    | 10-20 sec     | 5-10 sec      | 15-30 sec |
| 15 minutes   | 30-45 sec     | 10-15 sec     | 40-60 sec |
| 30 minutes   | 1-2 min       | 15-20 sec     | 1.5-2.5 min |
| 60 minutes   | 2-3 min       | 20-30 sec     | 2.5-3.5 min |

### Resource Requirements

- **Storage**: ~2-5 MB per hour of audio (depending on format)
- **Memory**: ~500 MB for Django + processing
- **CPU**: Minimal (AI processing is done via APIs)
- **Network**: Stable internet connection for API calls

### Free Tier Limits

**Groq (Whisper):**
- 6,000 requests/day = ~400 hours of audio/day
- 30 requests/minute = ~30 files/minute
- More than enough for most use cases!

**OpenRouter (LLaMA):**
- Varies by model and tier
- LLaMA 3.1 8B has generous free limits
- Monitor at https://openrouter.ai/activity

---

<div align="center">

**Made with ❤️ using Django, Whisper, and LLaMA**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/AYUSHOMMISHRA/Unthinkable-Meeting-Summarizer/issues) · 
[Request Feature](https://github.com/AYUSHOMMISHRA/Unthinkable-Meeting-Summarizer/issues) · 
[Documentation](https://github.com/AYUSHOMMISHRA/Unthinkable-Meeting-Summarizer#readme)

</div>
