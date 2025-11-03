# Resume Prompt for Legal Advisory v8.0

Copy and paste this prompt when starting a new session to provide full context:

---

## 📋 PROMPT TO COPY:

```
I'm working on the Legal Advisory System v8.0 project. This is a zero-hallucination legal AI system that's currently deployed to production. Before we continue, please:

1. Read the comprehensive project status:
   - Location: /home/claude/legal-advisory-v8/PROJECT_STATUS.md
   - This file contains: deployment URLs, architecture, configuration, issues fixed, troubleshooting guide, and next steps

2. Here's the quick context:

**Project Overview:**
- A legal advisory system with clarifying questions and case law verification
- Zero-hallucination architecture (<2% error rate)
- Covers Singapore legal procedures (Order 5, 14, 21)

**Current Deployment Status:**
- GitHub: https://github.com/Koulsami/legal-advisory-v8 ✅ LIVE
- Backend: https://legal-advisory-v8-production.up.railway.app ✅ DEPLOYED
- Frontend: Static files ready for Netlify deployment
- Last updated: November 3, 2025

**Technology Stack:**
- Backend: FastAPI + Python 3.12 on Railway
- Frontend: HTML/CSS/JS on Netlify
- AI: Anthropic Claude (Sonnet 4.5 + Haiku)
- Database: In-memory (6D logic tree)

**Recent Fixes Applied:**
1. Removed API keys from git commits (security)
2. Fixed Railway Procfile (removed cd backend command)
3. Fixed CORS configuration (allow_origins=["*"])
4. Backend successfully deployed and responding

**Key Files to Know:**
- `/home/claude/legal-advisory-v8/PROJECT_STATUS.md` - Complete status (READ THIS FIRST!)
- `/home/claude/legal-advisory-v8/backend/main.py` - FastAPI backend entry point
- `/home/claude/legal-advisory-v8/frontend/app.js` - Frontend application
- `/home/claude/legal-advisory-v8/DEPLOYMENT.md` - Deployment guide

**Environment:**
- Working directory: /home/claude/legal-advisory-v8
- Git repo initialized: Yes, branch: main
- Remote: https://github.com/Koulsami/legal-advisory-v8.git

**What's Working:**
✅ Backend API deployed on Railway
✅ Health endpoint returns 200 OK
✅ CORS configured for frontend access
✅ API key secured in Railway environment
✅ All code committed and pushed to GitHub
✅ Frontend code ready for deployment

**What I Need Help With:**
[Describe what you want to work on, for example:]
- Deploy frontend to Netlify
- Debug a specific issue
- Add new features
- Review deployment status
- [Your specific task here]

Please read PROJECT_STATUS.md first, then let me know you're ready to help with [your task].
```

---

## 📝 INSTRUCTIONS FOR USE:

1. **Copy the prompt above** (everything between the ``` marks)
2. **Paste it at the start of your new session**
3. **Add your specific task** in the "What I Need Help With" section
4. **Send the message**

The AI will read PROJECT_STATUS.md and immediately have full context about:
- Current deployment state
- Architecture and configuration
- Issues already fixed
- What's working and what's not
- Next steps and enhancements

---

## 🎯 EXAMPLE PROMPTS FOR DIFFERENT SCENARIOS:

### Scenario 1: Continue Deployment
```
[Paste main prompt above, then add:]

What I Need Help With:
- Deploy the frontend to Netlify
- Test the end-to-end system
- Verify all components are working together
```

### Scenario 2: Debug an Issue
```
[Paste main prompt above, then add:]

What I Need Help With:
- Frontend is showing error: [paste error message]
- I need help debugging this issue
- Backend logs show: [paste relevant logs if available]
```

### Scenario 3: Add New Features
```
[Paste main prompt above, then add:]

What I Need Help With:
- Add a new legal module for [specific legal area]
- Enhance the clarifying questions feature
- Implement [specific feature from PROJECT_PLAN.md]
```

### Scenario 4: Review and Optimize
```
[Paste main prompt above, then add:]

What I Need Help With:
- Review the current deployment for optimization opportunities
- Check if there are any security concerns
- Suggest performance improvements
```

### Scenario 5: Production Issues
```
[Paste main prompt above, then add:]

What I Need Help With:
- Backend is returning 500 errors
- Frontend can't connect to backend
- Railway deployment failed with: [error message]
- Netlify build failed with: [error message]
```

---

## ⚡ QUICK START CHECKLIST:

Before asking for help, you can quickly verify the system status yourself:

```bash
# 1. Navigate to project
cd /home/claude/legal-advisory-v8

# 2. Check git status
git status
git log --oneline -3

# 3. Test backend health
curl https://legal-advisory-v8-production.up.railway.app/api/health

# 4. Check if services are running (local dev)
docker-compose ps

# 5. Read the status file
cat PROJECT_STATUS.md | head -100
```

Include the output of any of these commands in your prompt if relevant to your issue.

---

## 🔑 IMPORTANT REMINDERS:

1. **API Key Security:**
   - The Anthropic API key is stored in Railway environment variables
   - It's NOT in git (protected by .gitignore)
   - The key is in `/home/claude/legal-advisory-v8/.env` locally
   - Never share the actual key in prompts or logs

2. **Project Location:**
   - Always work from: `/home/claude/legal-advisory-v8`
   - Don't confuse with the old v6.5 at `/home/claude/legal-advisory-v5`

3. **Deployment URLs:**
   - Backend: https://legal-advisory-v8-production.up.railway.app
   - Frontend: [Will be set after Netlify deployment]
   - GitHub: https://github.com/Koulsami/legal-advisory-v8

4. **Status Files to Reference:**
   - `PROJECT_STATUS.md` - Complete current state
   - `DEPLOYMENT.md` - Deployment instructions
   - `PROJECT_PLAN.md` - Long-term roadmap
   - `ENHANCEMENT_SUMMARY.md` - Recent features

---

## 📊 ONE-LINE STATUS CHECK:

If you just want a super quick check, use this compact prompt:

```
Quick status check for legal-advisory-v8 at /home/claude/legal-advisory-v8:
Please read PROJECT_STATUS.md and tell me:
1. Current deployment status (Backend/Frontend/GitHub)
2. Any issues that need attention
3. What's the next logical step

Then wait for my instructions on what to work on.
```

---

## 🎓 FOR THE AI ASSISTANT:

When you receive this prompt:
1. ✅ Read `/home/claude/legal-advisory-v8/PROJECT_STATUS.md` FIRST
2. ✅ Acknowledge what you've learned from it
3. ✅ Summarize the current state briefly
4. ✅ Ask clarifying questions if needed
5. ✅ Then proceed with the user's specific task

Do NOT:
- ❌ Start making changes without reading PROJECT_STATUS.md
- ❌ Ask for information that's already in PROJECT_STATUS.md
- ❌ Assume old context from previous conversations
- ❌ Guess at the deployment status

---

## 📞 ESCALATION PATHS:

If the AI assistant seems confused or not finding the status file:

**Step 1:** Verify file exists
```bash
ls -la /home/claude/legal-advisory-v8/PROJECT_STATUS.md
```

**Step 2:** Show first 50 lines directly in prompt
```bash
head -50 /home/claude/legal-advisory-v8/PROJECT_STATUS.md
```

**Step 3:** Paste the "Current State Summary" section manually

---

**Last Updated:** November 3, 2025
**Document Version:** 1.0
**Status:** Ready for use

---

**Pro Tip:** Bookmark this file or keep it open in a text editor for quick copy-paste access!
