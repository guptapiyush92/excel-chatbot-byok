# 🚀 Quick Start - Setup on Fresh System

Setting up this Excel Chatbot on a system with no development tools? Follow these simple steps!

---

## 📋 What You'll Need

1. **Your GitHub repository URL**
2. **30 minutes** of time
3. **Internet connection**
4. One **API key** (Anthropic, Google Gemini, or OpenAI)

---

## 🎯 One-Command Setup

### For macOS/Linux:

```bash
# 1. Clone the repository
git clone YOUR_GITHUB_REPO_URL
cd excel_chatbot

# 2. Run the setup script
bash quick_setup.sh

# 3. Run the app
source venv/bin/activate
streamlit run ui/chatbot_byok_ui.py
```

### For Windows:

```bash
# 1. Clone the repository
git clone YOUR_GITHUB_REPO_URL
cd excel_chatbot

# 2. Run the setup script (double-click or run in cmd)
quick_setup.bat

# 3. Run the app
venv\Scripts\activate
streamlit run ui/chatbot_byok_ui.py
```

**Then open:** http://localhost:8501

---

## 📖 Detailed Instructions

If you don't have Python or Git installed, see the **[Complete Setup Guide](SETUP_FROM_SCRATCH.md)** which covers:

- ✅ Installing Python from scratch
- ✅ Installing Git
- ✅ Setting up the project
- ✅ Getting API keys
- ✅ Running the application
- ✅ Troubleshooting common issues

---

## 🔑 API Keys

You need ONE of these (free tiers available!):

| Provider | Free Tier | Get Key |
|----------|-----------|---------|
| 🟢 **Google Gemini** | ✅ Yes | [Get Key](https://makersuite.google.com/app/apikey) |
| 🔷 **Anthropic Claude** | Limited | [Get Key](https://console.anthropic.com/) |
| 🟦 **OpenAI GPT** | Limited | [Get Key](https://platform.openai.com/api-keys) |

**For BYOK mode**: Users enter their keys in the UI (no setup needed)
**For Proxy mode**: Add your key to the `.env` file

---

## 🎮 Two Modes

### BYOK Mode (Recommended)
```bash
streamlit run ui/chatbot_byok_ui.py
```
- Users provide their own API keys
- No cost to you
- Users choose: Claude, Gemini, or GPT

### Proxy Mode
```bash
streamlit run ui/chatbot_upload_ui.py
```
- You provide the API key in `.env`
- Users don't need accounts
- You pay for usage

---

## 🆘 Need Help?

1. **Complete setup guide**: [SETUP_FROM_SCRATCH.md](SETUP_FROM_SCRATCH.md)
2. **Common issues**: Check the Troubleshooting section in the setup guide
3. **Python not found?** Make sure you installed Python and added it to PATH

---

## ⚡ Quick Commands Reference

```bash
# First time setup
git clone YOUR_REPO_URL
cd excel_chatbot
bash quick_setup.sh  # or quick_setup.bat on Windows

# Every time you run it
cd excel_chatbot
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run ui/chatbot_byok_ui.py

# Stop the app
Ctrl + C

# Update the app
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 💻 System Requirements

- **Python 3.10+** (3.11 recommended)
- **4GB RAM** minimum
- **2GB disk space** for dependencies
- **Windows 10+** / **macOS 10.15+** / **Ubuntu 20.04+**

---

## 🌐 Network Issues at Work?

If you're behind a corporate firewall and the Streamlit Cloud deployment isn't working, running it locally (following this guide) will bypass those restrictions!

---

**Ready? Start with the [Complete Setup Guide](SETUP_FROM_SCRATCH.md)!** 🚀
