# Deploy ChurnGuard Pro on Render.com

Complete guide to deploy ChurnGuard Pro on Render.com (Free tier available).

---

## Why Render.com?

✅ **Free tier** - Deploy both frontend & backend free  
✅ **Custom domain** - indigoairlineschurnguardpro.com  
✅ **Auto-deploy** - Git push → Automatic deployment  
✅ **SSL/HTTPS** - Free Let's Encrypt certificates  
✅ **Easy setup** - No Docker, no AWS complexity  
✅ **Environment variables** - Built-in secrets management  

---

## Step 1: Create Render Account

1. Go to https://dashboard.render.com
2. Sign up with **GitHub** (recommended - auto-connects repo)
3. Authorize GitHub access
4. ✅ Account created

---

## Step 2: Deploy Backend API

### Create Web Service

1. Render Dashboard → **New +** → **Web Service**
2. Click **Connect Repository**
3. Search: `ChurnGuard-Pro` → Click **Connect**
4. **Configure:**
   - **Name**: `churnguard-api`
   - **Root Directory**: `backend` ← Important!
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

5. **Environment Variables:**
   - Add variables if needed (none required for this app)

6. **Plan**: Free (or Starter for better performance)

7. Click **Create Web Service** → 🚀 Backend deploying...

**Get Backend URL** (looks like: `https://churnguard-api.onrender.com`)

---

## Step 3: Deploy Frontend

### Create Static Site

1. Render Dashboard → **New +** → **Static Site**
2. Click **Connect Repository**
3. Search: `ChurnGuard-Pro` → Click **Connect**
4. **Configure:**
   - **Name**: `churnguard-pro`
   - **Root Directory**: `frontend` ← Important!
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

5. Click **Create Static Site** → 🚀 Frontend deploying...

**Get Frontend URL** (looks like: `https://churnguard-pro.onrender.com`)

---

## Step 4: Update Frontend to Use Deployed Backend

The frontend needs to know the backend URL. Update this file:

**File: `frontend/src/App.jsx`**

Find this section (around line 100):
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

Replace with:
```javascript
const API_URL = typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : 'https://churnguard-api.onrender.com';
```

Or simpler - just use:
```javascript
const API_URL = 'https://churnguard-api.onrender.com';
```

**Commit and push:**
```bash
git add frontend/src/App.jsx
git commit -m "Update API URL for Render deployment"
git push origin main
```

Frontend will **auto-rebuild** on Render.

---

## Step 5: Connect Custom Domain

### Add subdomain to Render

1. **Frontend** → Settings → **Custom Domain**
   - Enter: `indigoairlineschurnguardpro.com`
   - Click **Add Custom Domain**

2. Render shows **CNAME**: `churnguard-pro.onrender.com`

### Update Domain DNS Settings

**If using Namecheap/GoDaddy:**

1. Go to domain settings
2. Find **DNS/Nameservers** section
3. Add **CNAME Record**:
   - **Host**: `indigoairlineschurnguardpro.com`
   - **Points to**: `churnguard-pro.onrender.com`
   - **TTL**: 3600

4. Wait **5-10 minutes** for DNS propagation

**If using Route 53:**

1. Route 53 → Hosted Zones → Your domain
2. Create **CNAME Record**:
   - **Name**: `indigoairlineschurnguardpro.com`
   - **Type**: CNAME
   - **Value**: `churnguard-pro.onrender.com`

---

## Step 6: Verify Deployment

### Check Backend

```bash
# Test health endpoint
curl https://churnguard-api.onrender.com/api/health

# Should return:
# {"status":"healthy","service":"ChurnGuard Pro API","version":"1.0.0"}
```

### Check Frontend

Visit: **https://indigoairlineschurnguardpro.com**

You should see:
- ✅ Indigo Airlines logo animation
- ✅ ChurnGuard Pro dashboard
- ✅ Green lock icon (HTTPS/SSL)

---

## Step 7: Configure Email (Optional)

For SSL renewal & notifications:

1. **Backend** → Click `churnguard-api`
2. Go to **Settings** → **Environment**
3. (Already using Let's Encrypt - no config needed)

---

## Deployment Summary

| Component | URL | Status |
|-----------|-----|--------|
| **Frontend** | https://indigoairlineschurnguardpro.com | 🟢 Live |
| **Backend API** | https://churnguard-api.onrender.com | 🟢 Live |
| **Repository** | https://github.com/sprabh12029-prsh/ChurnGuard-Pro | 📦 Connected |
| **Domain** | indigoairlineschurnguardpro.com | 🌍 Custom |
| **SSL Certificate** | Let's Encrypt (Auto-renews) | 🔒 Secure |

---

## Important Notes

### Free Tier Limits (Render)

- ✅ **Compute time**: 750 hours/month (sufficient for always-on)
- ✅ **Build time**: Unlimited
- ✅ **Static sites**: Always free
- ✅ **Web services**: Spins down after 15 min inactivity (wakes up on request)

**To keep backend always active:**
- Upgrade from Free to **Starter Plan** ($7/month)
- Or use free tier (slight delay on first request)

### Auto-Deploy on Git Push

Every time you push to `main`:
1. Render detects the change
2. Automatically rebuilds
3. Redeploys both frontend & backend
4. **Zero downtime**

### Environment Variables

To add secrets (API keys, database URLs, etc.):

1. Service → **Settings** → **Environment**
2. Add variables in dashboard
3. No need to commit secrets to git

---

## Troubleshooting

### Frontend shows blank page
- Check browser console for errors (F12)
- Verify backend URL is correct in App.jsx
- Render dashboard → Logs tab

### Backend returning 404
- Check logs in Render dashboard
- Verify service is running (not spun down)
- Check environment variables

### Can't reach domain
- Wait 5-10 minutes for DNS propagation
- Check DNS records in domain registrar
- Clear browser cache (Ctrl+Shift+Delete)

### Backend responding slow
- Free tier spins down after 15 min - first request is slow
- Upgrade to Starter Plan for consistent performance

---

## Next Steps

1. ✅ Create Render account
2. ✅ Deploy backend to Render
3. ✅ Deploy frontend to Render
4. ✅ Update frontend API URL
5. ✅ Add custom domain
6. ✅ Configure DNS
7. ✅ Test application
8. ✅ Celebrate! 🎉

Your ChurnGuard Pro is now **live globally** with auto-deploy on every git push!

---

## Support & Docs

- **Render Docs**: https://render.com/docs
- **GitHub Integration**: https://render.com/docs/github
- **Custom Domains**: https://render.com/docs/custom-domains
- **Environment Variables**: https://render.com/docs/environment-variables

