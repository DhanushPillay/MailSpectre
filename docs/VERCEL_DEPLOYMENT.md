# MailSpectre - Vercel Deployment Guide 🚀

## Quick Deploy to Vercel

### Step 1: Install Vercel CLI (if not already installed)
```bash
npm i -g vercel
```

### Step 2: Deploy
```bash
# From your project root
vercel
```

That's it! Vercel will:
- ✅ Detect the configuration from `vercel.json`
- ✅ Deploy frontend (HTML/CSS/JS) as static files
- ✅ Deploy backend (Python Flask) as serverless functions
- ✅ Both will run on the **same domain** (no CORS issues!)

---

## How It Works

### Project Structure for Vercel:
```
MailSpectre/
├── api/
│   └── index.py          ← Backend entry point for Vercel
├── backend/
│   ├── app.py            ← Your Flask app
│   ├── checker.py        ← Email validation logic
│   ├── requirements.txt  ← Python dependencies
│   └── DATA/             ← Fraud & company data
├── frontend/
│   ├── index.html        ← Main page
│   ├── script.js         ← Frontend logic
│   └── styles.css        ← Styling
├── vercel.json           ← Vercel configuration
└── README.md
```

### What Happens on Vercel:

1. **Frontend Routes** (`/`, `/index.html`):
   - Served from `frontend/` folder
   - Static HTML/CSS/JS files
   - Fast CDN delivery

2. **API Routes** (`/api/*`):
   - Handled by `api/index.py`
   - Imports your Flask app from `backend/`
   - Runs as serverless function
   - Auto-scales with traffic

3. **Backend Auto-Start**:
   - ❌ No `python app.py` needed!
   - ✅ Vercel runs Flask as serverless function
   - ✅ Automatically starts on every request
   - ✅ Scales to zero when not in use (saves resources)

---

## Configuration Files

### ✅ `vercel.json` (Already Created)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

### ✅ `api/index.py` (Already Created)
- Entry point for backend
- Imports your Flask app
- Vercel calls this for API requests

### ✅ `frontend/script.js` (Already Updated)
- Detects if running locally or on Vercel
- Uses correct API URL automatically:
  - Local: `http://localhost:5000`
  - Vercel: Same domain (relative path)

---

## Deployment Steps

### First Time Deploy:
```bash
# 1. Login to Vercel
vercel login

# 2. Deploy
cd "E:\Personal Projects\MailSpectre"
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? mailspectre
# - Directory? ./
# - Override settings? No
```

### Update After Changes:
```bash
# Just run
vercel --prod
```

---

## Environment Variables (Optional)

If you need environment variables:

```bash
# Set via CLI
vercel env add FLASK_ENV production

# Or in Vercel Dashboard:
# Project Settings → Environment Variables
```

---

## Testing After Deploy

1. Vercel gives you a URL like: `https://mailspectre.vercel.app`

2. Visit the URL:
   - Frontend loads
   - Status shows "🟢 Backend Online"
   - Enter email and click Inspect
   - Results appear!

3. API endpoints available at:
   - `https://mailspectre.vercel.app/api/validate`
   - `https://mailspectre.vercel.app/api/health`

---

## Key Benefits

✅ **Auto-Start**: Backend runs automatically on every API call
✅ **No Server Management**: Vercel handles everything
✅ **Auto-Scaling**: Handles any traffic level
✅ **Same Domain**: No CORS issues
✅ **Free Tier**: Plenty for personal projects
✅ **Global CDN**: Fast worldwide
✅ **HTTPS**: Free SSL certificate

---

## Cost

**Vercel Free Tier Includes:**
- Unlimited deployments
- 100 GB bandwidth/month
- Serverless function executions
- Custom domain support
- HTTPS

**More than enough for MailSpectre!**

---

## Troubleshooting

**If backend doesn't work:**

1. Check logs:
```bash
vercel logs
```

2. Verify build:
```bash
vercel build
```

3. Check `requirements.txt` is in `backend/` folder

4. Ensure `api/index.py` imports correctly

---

## Custom Domain (Optional)

```bash
# Add your domain
vercel domains add yourdomain.com

# Vercel will show DNS settings to add
```

---

## Next Steps After Deploy

1. ✅ Test all features
2. ✅ Update README with live URL
3. ✅ Share with friends!
4. ✅ Monitor usage in Vercel dashboard

---

**Ready to deploy? Run: `vercel`** 🚀
