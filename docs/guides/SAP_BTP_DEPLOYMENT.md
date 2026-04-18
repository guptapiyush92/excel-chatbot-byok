# SAP BTP Cloud Foundry Deployment Guide

## 🎯 Perfect for Your POC!

SAP BTP Cloud Foundry is ideal for enterprise demos and POCs. This guide will help you deploy the Excel Chatbot.

---

## 📋 Prerequisites

### 1. SAP BTP Account
- Free trial account at: https://account.hanatrial.ondemand.com/
- Or use your company's SAP BTP account

### 2. Cloud Foundry CLI
Install the CF CLI tool:

**macOS:**
```bash
brew install cloudfoundry/tap/cf-cli
```

**Windows:**
Download from: https://github.com/cloudfoundry/cli/releases

**Linux:**
```bash
wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
echo "deb https://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
sudo apt-get update
sudo apt-get install cf-cli
```

**Verify installation:**
```bash
cf --version
```

---

## 🚀 Deployment Steps

### Step 1: Login to SAP BTP

```bash
# Login to SAP BTP Cloud Foundry
cf login -a https://api.cf.eu10.hana.ondemand.com

# You'll be prompted for:
# - Email: your-email@company.com
# - Password: your-password
# - Org: (select your org)
# - Space: (select dev or create new)
```

**Other API endpoints:**
- EU10: `https://api.cf.eu10.hana.ondemand.com`
- US10: `https://api.cf.us10.hana.ondemand.com`
- AP21: `https://api.cf.ap21.hana.ondemand.com`

Choose the one matching your BTP account region.

### Step 2: Verify Your Target

```bash
cf target
```

Should show:
```
API endpoint:   https://api.cf.eu10.hana.ondemand.com
Org:            your-org
Space:          dev
```

### Step 3: Deploy the Application

From your project directory:

```bash
# Navigate to project root
cd /Users/I307426/Documents/IECOE/Projects/excel_chatbot

# Push to Cloud Foundry
cf push excel-chatbot
```

**That's it!** The deployment will:
1. Upload your application (excludes venv, chroma_db automatically)
2. Detect Python buildpack
3. Install dependencies from requirements.txt
4. Start the application
5. Assign a public URL

### Step 4: Get Your Application URL

```bash
cf apps
```

You'll see output like:
```
name             state     instances   memory   disk   urls
excel-chatbot    started   1/1         1G       1G     excel-chatbot-happy-impala.cfapps.eu10.hana.ondemand.com
```

**Your URL:** `https://excel-chatbot-happy-impala.cfapps.eu10.hana.ondemand.com`

---

## 🎯 For POC/Demo

### Before Your Meeting:

1. **Deploy:**
   ```bash
   cf push excel-chatbot
   ```

2. **Test URL:** Open in browser and verify

3. **Keep app running:**
   ```bash
   cf app excel-chatbot
   ```

### During Meeting:

1. Open your BTP URL
2. Upload Excel file
3. Demo queries with rich formatting
4. Share URL with attendees

---

## 📊 Configuration Options

### Increase Memory (if needed)

Edit `manifest.yml`:
```yaml
applications:
- name: excel-chatbot
  memory: 2G  # Increase from 1G to 2G
```

Then redeploy:
```bash
cf push excel-chatbot
```

### Scale Instances

```bash
# Scale to 2 instances
cf scale excel-chatbot -i 2

# Or edit manifest.yml
instances: 2
```

### Set Environment Variables

```bash
# Set environment variable
cf set-env excel-chatbot API_HOST "0.0.0.0"

# Restart app
cf restart excel-chatbot
```

---

## 🔍 Monitoring & Logs

### View Logs (Real-time)

```bash
cf logs excel-chatbot
```

### View Recent Logs

```bash
cf logs excel-chatbot --recent
```

### Check App Status

```bash
cf app excel-chatbot
```

### Check App Health

```bash
cf events excel-chatbot
```

---

## 🔧 Common Commands

### Restart Application
```bash
cf restart excel-chatbot
```

### Stop Application
```bash
cf stop excel-chatbot
```

### Start Application
```bash
cf start excel-chatbot
```

### Delete Application
```bash
cf delete excel-chatbot
```

### Update Application (Redeploy)
```bash
# After making changes
cf push excel-chatbot
```

---

## 🐛 Troubleshooting

### Issue: "cf: command not found"
**Solution:** Install CF CLI (see Prerequisites)

### Issue: "No API endpoint set"
**Solution:**
```bash
cf api https://api.cf.eu10.hana.ondemand.com
cf login
```

### Issue: "Not enough memory"
**Solution:** Increase memory in manifest.yml:
```yaml
memory: 2G  # or 512M for minimal
```

### Issue: "Staging failed"
**Solution:** Check logs:
```bash
cf logs excel-chatbot --recent
```

Common fixes:
- Verify requirements.txt is present
- Check Python version in runtime.txt
- Ensure all imports work locally

### Issue: "App crashes after deployment"
**Solution:**
```bash
# Check logs
cf logs excel-chatbot --recent

# Common issues:
# - Port binding (should use $PORT)
# - Missing dependencies
# - Import errors
```

### Issue: "Cannot access URL"
**Solution:**
```bash
# Check routes
cf routes

# Check app is running
cf app excel-chatbot
```

---

## 💰 SAP BTP Free Trial Limits

**Free Tier Includes:**
- 2GB Cloud Foundry Runtime
- 4GB Application Runtime Memory
- Perfect for POC/Demo!

**Your App Uses:**
- 1GB memory (configurable)
- 1 instance
- Well within free tier ✅

---

## 🔒 Security Considerations

### For Production:

1. **Custom Domain:**
   ```bash
   cf map-route excel-chatbot your-domain.com --hostname excel-chatbot
   ```

2. **Add Authentication:**
   - Use SAP BTP XSUAA service
   - Or implement custom auth in app

3. **HTTPS Only:**
   - BTP provides HTTPS by default ✅

4. **Environment Variables:**
   ```bash
   cf set-env excel-chatbot SECRET_KEY "your-secret"
   ```

---

## 📁 What Gets Deployed

**Included:**
- ✅ api/ folder
- ✅ ui/ folder
- ✅ src/ folder
- ✅ requirements.txt
- ✅ manifest.yml
- ✅ runtime.txt
- ✅ Procfile

**Excluded (via .cfignore):**
- ❌ venv/
- ❌ .venv/
- ❌ chroma_db/
- ❌ .git/
- ❌ __pycache__/
- ❌ *.pyc

---

## 🎨 Custom Configuration

### Custom App Name

Edit `manifest.yml`:
```yaml
applications:
- name: my-excel-chatbot  # Change name
```

### Custom Memory/Disk

```yaml
applications:
- name: excel-chatbot
  memory: 512M      # Reduce for free tier
  disk_quota: 512M  # Limit disk usage
```

### Custom Python Version

Edit `runtime.txt`:
```
python-3.10.x
```

---

## 🔄 CI/CD Integration

### Manual Deployment
```bash
git pull origin main
cf push excel-chatbot
```

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to SAP BTP

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Install CF CLI
      run: |
        wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
        echo "deb https://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
        sudo apt-get update
        sudo apt-get install cf-cli
    - name: Deploy
      run: |
        cf login -a ${{ secrets.CF_API }} -u ${{ secrets.CF_USERNAME }} -p ${{ secrets.CF_PASSWORD }} -o ${{ secrets.CF_ORG }} -s ${{ secrets.CF_SPACE }}
        cf push excel-chatbot
```

---

## 📚 Additional Resources

- **SAP BTP Documentation:** https://help.sap.com/btp
- **Cloud Foundry Docs:** https://docs.cloudfoundry.org/
- **Python Buildpack:** https://docs.cloudfoundry.org/buildpacks/python/

---

## ✅ Quick Checklist

**Before Deployment:**
- [ ] CF CLI installed
- [ ] Logged into SAP BTP
- [ ] In correct org and space
- [ ] manifest.yml exists
- [ ] requirements.txt exists

**After Deployment:**
- [ ] App shows "started" state
- [ ] URL is accessible
- [ ] Can upload Excel files
- [ ] Queries work correctly
- [ ] Rich formatting displays

---

## 🎯 Quick Reference

```bash
# Login
cf login -a https://api.cf.eu10.hana.ondemand.com

# Deploy
cf push excel-chatbot

# Check status
cf app excel-chatbot

# View logs
cf logs excel-chatbot --recent

# Get URL
cf apps

# Restart
cf restart excel-chatbot

# Delete
cf delete excel-chatbot
```

---

## 💡 Pro Tips

1. **Test locally first:**
   ```bash
   bash scripts/run_api.sh
   ```

2. **Check manifest before push:**
   ```bash
   cat manifest.yml
   ```

3. **Monitor first deployment:**
   ```bash
   cf push excel-chatbot & cf logs excel-chatbot
   ```

4. **Use descriptive app names:**
   - `excel-chatbot-dev`
   - `excel-chatbot-poc`
   - `excel-chatbot-prod`

---

**Your Excel Chatbot is ready for SAP BTP deployment!** 🚀

The free trial is perfect for POCs and demos. Deploy now with `cf push excel-chatbot`!
