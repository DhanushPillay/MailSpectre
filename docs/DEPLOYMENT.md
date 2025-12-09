# MailSpectre Deployment Guide 🚀

## Quick Deploy Options

### Option 1: Render.com (Recommended - FREE)

**Backend Deployment:**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** mailspectre-backend
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click "Create Web Service"

**Frontend Deployment:**
1. Click "New +" → "Static Site"
2. Connect same GitHub repo
3. Configure:
   - **Name:** mailspectre-frontend
   - **Root Directory:** `frontend`
   - **Build Command:** (leave empty)
   - **Publish Directory:** `.`
4. Click "Create Static Site"

**Update Frontend:**
After backend is deployed, edit `frontend/script.js`:
```javascript
const CONFIG = {
    API_BASE_URL: 'https://mailspectre-backend.onrender.com',  // ← Your backend URL
    API_ENDPOINT: '/api/validate',
    REQUEST_TIMEOUT: 10000
};
```

---

### Option 2: Vercel (Frontend) + Render (Backend)

**Backend on Render:** (Same as above)

**Frontend on Vercel:**
1. Install Vercel CLI: `npm i -g vercel`
2. In frontend folder: `vercel`
3. Follow prompts
4. Update API URL in `script.js`

---

### Option 3: Railway.app (Easiest - One Platform)

**Deploy Both:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Railway auto-detects Python backend
4. Add environment variables if needed
5. Backend starts automatically!

---

### Option 4: Heroku

**Backend:**
1. Install Heroku CLI
2. Commands:
```bash
cd backend
heroku login
heroku create mailspectre-backend
git push heroku main
```

**Frontend:**
- Deploy to Netlify/Vercel
- Update API URL

---

## Environment Variables (If Needed)

For production, you might want:
```
FLASK_ENV=production
DEBUG=False
CORS_ORIGIN=https://your-frontend-url.com
```

---

## How Backend Stays Running

**Local Development:**
- YOU manually run: `python app.py`
- Server stops when you close terminal

**Production (Render/Heroku/Railway):**
- Platform runs: `gunicorn app:app`
- Server runs 24/7 automatically
- Auto-restarts if it crashes
- Scales automatically with traffic

---

## Files for Deployment

✅ **Already Created:**
- `requirements.txt` - Python dependencies
- `Procfile` - Tells server how to start backend
- `runtime.txt` - Specifies Python version

✅ **Need to Update:**
- `frontend/script.js` - Change API_BASE_URL to deployed backend URL

---

## Cost

**FREE Options:**
- **Render:** 750 hours/month free (enough for 24/7)
- **Railway:** $5 credit/month (covers small app)
- **Vercel:** Unlimited for frontend
- **Netlify:** Unlimited for frontend

---

## Quick Summary

**In Production:**
1. ✅ Platform starts backend automatically using `gunicorn`
2. ✅ Backend runs 24/7 (no manual start needed)
3. ✅ Auto-restarts if crashes
4. ✅ Frontend connects to backend via HTTPS URL
5. ✅ No need to open terminal or run commands!

**The magic:**
- `Procfile` tells platform: "Start backend with `gunicorn app:app`"
- Platform reads it and keeps your backend running forever!

---

## Test After Deployment

1. Visit your frontend URL
2. Backend status should show "🟢 Backend Online"
3. Enter email and click Inspect
4. Results appear - you're live! 🎉

---

**Need help deploying? Let me know which platform you want to use!**
