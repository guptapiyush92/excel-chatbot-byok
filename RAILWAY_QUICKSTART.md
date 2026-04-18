# Railway.app Quick Deployment - POC Guide

## 🚀 5-Minute Deployment

### **Step 1: Go to Railway**
```
https://railway.app/
```

### **Step 2: Login**
- Click **"Login"**
- Choose **"Login with GitHub"**
- Authorize Railway

### **Step 3: Deploy**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: **`guptapiyush92/excel-chatbot-byok`**
4. Railway auto-detects Python ✅

### **Step 4: Configure Start Command**
1. Click on your deployment
2. Go to **Settings** tab
3. Scroll to **"Deploy"** section
4. Set **Start Command:**
   ```
   uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **"Save"**

### **Step 5: Generate Public URL**
1. Stay in **Settings** tab
2. Find **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your URL (e.g., `https://excel-chatbot-byok-production.up.railway.app`)

### **Step 6: Wait for Deployment**
- Go to **"Deployments"** tab
- Watch for **"SUCCESS"** status
- Takes ~5-10 minutes

### **Step 7: Test**
- Open your Railway URL
- Upload Excel file
- Test queries
- Share URL for POC! 🎉

---

## 📱 **For Your POC Presentation**

### **Before Meeting:**
- [ ] Deploy to Railway (done above)
- [ ] Test URL works
- [ ] Upload sample Excel file
- [ ] Prepare sample queries

### **During Meeting:**
- [ ] Open Railway URL on presentation laptop
- [ ] Demo file upload
- [ ] Show rich formatting (tables, code blocks)
- [ ] Answer questions with live queries

### **Share with Attendees:**
Give them the Railway URL - they can try it live!

---

## ⚡ **Quick Commands**

**View Logs:**
- Railway Dashboard → Click deployment → "View Logs"

**Redeploy:**
- Push to GitHub → Auto-redeploys
- Or: Railway Dashboard → "Redeploy"

**Change Settings:**
- Railway Dashboard → Settings tab

---

## 🐛 **Common Issues**

### **"Application failed to respond"**
**Fix:** Check Start Command is correct:
```
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### **"Build failed"**
**Fix:** Check build logs. Usually missing dependencies.

### **"Domain not accessible"**
**Fix:** Wait 1-2 minutes after deployment completes.

---

## 💡 **Pro Tips**

1. **Keep Railway tab open** during demo to prevent cold starts
2. **Test 5 minutes before** your presentation
3. **Have backup plan** (screenshots) if network fails
4. **Railway URL is permanent** - use same URL for multiple demos

---

## 📊 **What You're Deploying**

✅ FastAPI backend with rich markdown formatting
✅ Tables, code highlighting, lists
✅ Multi-provider AI support (Claude, Gemini, GPT)
✅ Excel file upload and processing
✅ No WebSocket dependencies (firewall-friendly!)

---

## 🔗 **Your URLs**

**GitHub Repo:**
```
https://github.com/guptapiyush92/excel-chatbot-byok
```

**Railway URL (after deployment):**
```
https://YOUR-APP-NAME.up.railway.app
```

---

## ⏱️ **Timeline**

- **Now:** Deploy to Railway (5 min)
- **+10 min:** Test and verify
- **Ready:** Share URL for POC

---

**Good luck with your POC! 🚀**

Questions? Check Railway logs or redeploy from scratch.
