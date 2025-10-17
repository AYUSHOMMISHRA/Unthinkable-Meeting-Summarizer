# Railway Troubleshooting Guide

## Check 1: Verify Environment Variables are Set

Go to your Railway project dashboard and verify these variables are set:

```
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
DEBUG=False
```

Without these keys, processing will hang or fail silently.

## Check 2: View Railway Logs

In Railway dashboard:
1. Click on your deployment
2. Go to "Deployments" tab
3. Click on the latest deployment
4. Look for these error messages:
   - `decouple.UndefinedValueError: OPENAI_API_KEY not found`
   - `decouple.UndefinedValueError: GROQ_API_KEY not found`
   - Any timeout errors
   - Any API errors from OpenAI/Groq

## Check 3: Increase Gunicorn Timeout

The current Gunicorn timeout is 300 seconds (5 minutes), but worker threads may still be killed.

## Quick Fix: Set Environment Variables

If you haven't already, add these to Railway Variables:

```bash
OPENAI_API_KEY=<your-openrouter-or-openai-key>
GROQ_API_KEY=<your-groq-key>
DEBUG=False
OPENAI_TIMEOUT=600
```

## Long-term Solution: Use Celery

For production, you should use Celery with Redis for background task processing.
This ensures tasks complete even if the web worker is restarted.
