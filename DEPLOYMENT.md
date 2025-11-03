# Deployment Guide - Legal Advisory System v8.0

This guide will help you deploy the backend to Railway and frontend to Netlify using your GitHub account.

## Prerequisites

- GitHub account: **Samikoul**
- Railway account (sign up at https://railway.app)
- Netlify account (sign up at https://netlify.com)
- Anthropic API key

---

## Step 1: Push to GitHub

### 1.1 Create GitHub Repository

1. Go to https://github.com/Samikoul
2. Click "New repository"
3. Repository name: `legal-advisory-v8`
4. Description: "Legal Advisory System v8.0 - Zero-Hallucination Legal AI with Case Law Verification"
5. Choose **Public** or **Private**
6. **Do NOT initialize with README** (we already have one)
7. Click "Create repository"

### 1.2 Push Code to GitHub

The repository is already initialized with git and ready to push. Follow the instructions shown on GitHub after creating the repository, or use these commands:

```bash
cd /home/claude/legal-advisory-v8

# Add all files
git add .

# Commit
git commit -m "Initial commit: Legal Advisory System v8.0

Features:
- Three-stage retrieval with Elasticsearch
- Zero-hallucination architecture (<2%)
- Clarifying questions feature
- Case law verification with verbatim quotes
- Order 5, 14, and 21 integration
- Hybrid search (6D)
- Production-ready backend and frontend"

# Add remote (replace with your GitHub repository URL)
git remote add origin https://github.com/Samikoul/legal-advisory-v8.git

# Push to GitHub
git push -u origin main
```

---

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `Samikoul/legal-advisory-v8`
6. Railway will detect the `railway.json` and `nixpacks.toml` automatically

### 2.2 Configure Environment Variables

In the Railway project dashboard:

1. Click on your service
2. Go to "Variables" tab
3. Add the following environment variables:

**Required:**
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**Optional (Railway provides managed databases):**
```
PORT=8000
DEBUG=false
LOG_LEVEL=INFO
```

### 2.3 Set Root Directory

1. In Railway project settings
2. Go to "Settings" → "Deploy"
3. Set **Root Directory** to: `backend`
4. Save changes

### 2.4 Deploy

1. Railway will automatically deploy
2. Wait for deployment to complete (~3-5 minutes)
3. Copy the deployment URL (e.g., `https://your-app.railway.app`)
4. Test health endpoint: `https://your-app.railway.app/api/health`

### 2.5 Add Managed Services (Optional)

For production, you may want to add Railway managed databases:

1. In your project, click "New"
2. Add **PostgreSQL** database
3. Add **Redis** database
4. Railway will automatically inject connection variables

**Note:** Elasticsearch and Neo4j may need external hosting (e.g., Elastic Cloud, Neo4j Aura)

---

## Step 3: Deploy Frontend to Netlify

### 3.1 Create Netlify Site

1. Go to https://netlify.com
2. Sign in with GitHub
3. Click "Add new site" → "Import an existing project"
4. Choose "GitHub"
5. Select `Samikoul/legal-advisory-v8`

### 3.2 Configure Build Settings

**Build settings:**
- **Base directory:** `frontend`
- **Build command:** (leave empty - static site)
- **Publish directory:** `.` (or leave as `frontend`)

### 3.3 Update Frontend API URL

Before deploying, update the frontend to point to your Railway backend:

1. Edit `/home/claude/legal-advisory-v8/frontend/app.js`
2. Find line ~4:
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost'
       ? 'http://localhost:8000'
       : 'https://your-backend-url.railway.app'; // Update this!
   ```
3. Replace `https://your-backend-url.railway.app` with your actual Railway URL
4. Commit and push:
   ```bash
   git add frontend/app.js
   git commit -m "Update frontend API URL with Railway backend"
   git push
   ```

### 3.4 Deploy

1. Click "Deploy site"
2. Wait for deployment (~1-2 minutes)
3. Netlify will provide a URL like: `https://random-name-12345.netlify.app`

### 3.5 Configure Custom Domain (Optional)

In Netlify site settings:
1. Go to "Domain management"
2. Click "Add custom domain"
3. Follow instructions to configure DNS

---

## Step 4: Enable CORS on Backend

Update your backend to allow requests from the Netlify frontend:

1. Edit `backend/main.py`
2. Add your Netlify URL to CORS origins:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",
           "https://your-netlify-site.netlify.app",  # Add this
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
3. Commit and push
4. Railway will auto-deploy the update

---

## Step 5: Test Deployment

### 5.1 Test Backend

```bash
# Health check
curl https://your-app.railway.app/api/health

# Test query
curl -X POST https://your-app.railway.app/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are costs under Order 21?"}'
```

### 5.2 Test Frontend

1. Open your Netlify URL
2. Ask a question: "When can I get indemnity costs?"
3. Verify the response includes case law citations
4. Try a vague question: "I need costs information"
5. Verify clarifying questions appear

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│            Netlify Frontend                 │
│  https://legal-advisory.netlify.app         │
│                                             │
│  - Static HTML/CSS/JS                       │
│  - Zero-hallucination UI                    │
│  - Case law verification display            │
└─────────────────┬───────────────────────────┘
                  │
                  │ HTTPS/JSON
                  │
┌─────────────────▼───────────────────────────┐
│            Railway Backend                  │
│  https://legal-advisory.railway.app         │
│                                             │
│  - FastAPI + Python 3.12                    │
│  - Three-stage retrieval                    │
│  - Clarifying questions                     │
│  - Case law verification                    │
│  - Conversation management                  │
└─────────────────┬───────────────────────────┘
                  │
                  │ Anthropic API
                  │
┌─────────────────▼───────────────────────────┐
│         Claude (Anthropic)                  │
│  - Sonnet 4.5 for responses                 │
│  - Haiku for clarifying questions           │
└─────────────────────────────────────────────┘
```

---

## Environment Variables Reference

### Backend (Railway)

**Required:**
- `ANTHROPIC_API_KEY` - Your Anthropic API key

**Optional:**
- `PORT` - Port number (Railway sets automatically)
- `DEBUG` - Debug mode (default: false)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, WARNING, ERROR)

**Database (if using Railway managed services):**
- Railway auto-injects: `DATABASE_URL`, `REDIS_URL`

### Frontend (Netlify)

No environment variables needed - configuration is in `app.js`

---

## Monitoring & Logs

### Railway
- View logs: Project → Service → Logs tab
- Metrics: Project → Service → Metrics tab
- Health: Check `/api/health` endpoint

### Netlify
- View logs: Site → Deploys → Deploy log
- Analytics: Site → Analytics tab
- Forms: Site → Forms tab (if using)

---

## Troubleshooting

### Backend Issues

**Problem:** Health check fails
- **Solution:** Check Railway logs, verify `ANTHROPIC_API_KEY` is set

**Problem:** CORS errors
- **Solution:** Add Netlify URL to CORS origins in `main.py`

**Problem:** Database connection errors
- **Solution:** For now, backend works without databases (uses in-memory)
- **Future:** Add Railway managed PostgreSQL/Redis

### Frontend Issues

**Problem:** "Unable to connect to backend"
- **Solution:** Verify Railway backend URL in `frontend/app.js`

**Problem:** 404 errors on routes
- **Solution:** Ensure `netlify.toml` is present with redirect rules

---

## Cost Estimates

### Railway
- **Free tier:** $5 credit/month (sufficient for development)
- **Paid:** ~$5-20/month depending on usage

### Netlify
- **Free tier:** 100GB bandwidth, 300 build minutes/month
- **Paid:** $19/month for Pro features

### Anthropic API
- **Claude Sonnet 4.5:** $3 per million input tokens, $15 per million output tokens
- **Claude Haiku:** $0.25 per million input tokens, $1.25 per million output tokens
- **Estimated:** ~$10-50/month depending on usage

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy backend to Railway
3. ✅ Deploy frontend to Netlify
4. ✅ Update frontend with Railway URL
5. ✅ Configure CORS
6. ✅ Test deployment
7. 🔄 Monitor usage and costs
8. 🔄 Add custom domain (optional)
9. 🔄 Set up CI/CD (optional)
10. 🔄 Add production databases (optional)

---

## Support

- **Railway Docs:** https://docs.railway.app
- **Netlify Docs:** https://docs.netlify.com
- **Anthropic Docs:** https://docs.anthropic.com

---

**Deployment Status:** Ready for production
**Version:** 8.0
**Last Updated:** November 3, 2025
