# Complete Setup Guide - From Scratch

This guide will help you set up the Excel Chatbot on a completely fresh system with no development tools installed.

---

## Step 1: Install Python

### Windows
1. Go to https://www.python.org/downloads/
2. Download **Python 3.11** (recommended) or Python 3.10+
3. **IMPORTANT**: During installation, check ✅ **"Add Python to PATH"**
4. Click "Install Now"
5. Verify installation:
   - Open Command Prompt (cmd)
   - Type: `python --version`
   - Should show: `Python 3.11.x`

### macOS
1. Open Terminal (search "Terminal" in Spotlight)
2. Install Homebrew (package manager):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python@3.11
   ```
4. Verify: `python3 --version`

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3 --version
```

---

## Step 2: Install Git

### Windows
1. Go to https://git-scm.com/download/win
2. Download and install
3. Use default settings during installation
4. Verify: Open cmd and type `git --version`

### macOS
```bash
brew install git
```

### Linux
```bash
sudo apt install git
```

---

## Step 3: Clone the Repository

1. **Choose a location** for your project (e.g., Documents folder)
2. Open Terminal (macOS/Linux) or Command Prompt (Windows)
3. Navigate to your desired folder:
   ```bash
   cd Documents
   ```
4. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/excel_chatbot.git
   ```
   Replace `YOUR_USERNAME` with your actual GitHub username

5. Enter the project folder:
   ```bash
   cd excel_chatbot
   ```

---

## Step 4: Create Virtual Environment

A virtual environment keeps your project dependencies isolated.

### Windows (Command Prompt)
```bash
python -m venv venv
venv\Scripts\activate
```

### Windows (PowerShell)
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

If you get an error about execution policy:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` appear in your terminal prompt.**

---

## Step 5: Install Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 5-10 minutes. ☕

**Common Issues:**

- **"pip not found"**: Use `python -m pip` instead of `pip`
- **Permission denied**: Add `--user` flag: `pip install --user -r requirements.txt`
- **Timeout errors**: Try: `pip install --default-timeout=100 -r requirements.txt`

---

## Step 6: Get API Keys

You need at least ONE of these API keys:

### Option 1: Anthropic Claude (Recommended)
1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Go to "API Keys"
4. Create a new key
5. Copy the key (starts with `sk-ant-`)

### Option 2: Google Gemini (Free Tier Available!)
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### Option 3: OpenAI GPT
1. Go to https://platform.openai.com/api-keys
2. Sign up / Log in
3. Create new secret key
4. Copy the key (starts with `sk-`)

---

## Step 7: Configure API Key (Optional)

**For BYOK mode (recommended)**: Skip this step - users will enter their own keys in the UI.

**For Proxy mode** (you provide the key):

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

   On Windows:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file (use Notepad, TextEdit, or any text editor):
   ```
   ANTHROPIC_API_KEY=your_actual_key_here
   ```

---

## Step 8: Run the Application

### BYOK Mode (Users bring their own API keys)

**Windows:**
```bash
venv\Scripts\activate
streamlit run ui/chatbot_byok_ui.py
```

**macOS/Linux:**
```bash
source venv/bin/activate
streamlit run ui/chatbot_byok_ui.py
```

### Proxy Mode (You provide API key)

**Windows:**
```bash
venv\Scripts\activate
streamlit run ui/chatbot_upload_ui.py
```

**macOS/Linux:**
```bash
source venv/bin/activate
streamlit run ui/chatbot_upload_ui.py
```

---

## Step 9: Access the App

After running the command, you'll see:

```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

1. **Open your browser** (Chrome, Firefox, Safari, Edge)
2. Go to: **http://localhost:8501**
3. The app should load! 🎉

---

## Troubleshooting

### "Python not found" or "command not found"
- **Windows**: Use `python` instead of `python3`
- **macOS/Linux**: Use `python3` instead of `python`
- Make sure you checked "Add to PATH" during Python installation

### Port 8501 already in use
```bash
streamlit run ui/chatbot_byok_ui.py --server.port 8502
```

### ModuleNotFoundError
```bash
pip install [missing-module-name]
```

### ChromaDB / SQLite errors
```bash
pip uninstall chromadb
pip install chromadb --no-cache-dir
```

### Torch/Vision installation issues (Windows)
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Memory errors during installation
Install packages one by one:
```bash
pip install streamlit
pip install pandas openpyxl
pip install anthropic
pip install chromadb
# ... etc
```

---

## Daily Usage

Every time you want to run the app:

1. **Open Terminal/Command Prompt**
2. **Navigate to project folder:**
   ```bash
   cd Documents/excel_chatbot
   ```
3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. **Run the app:**
   ```bash
   streamlit run ui/chatbot_byok_ui.py
   ```
5. **Open browser:** http://localhost:8501

---

## Stopping the App

Press `Ctrl + C` in the terminal to stop the server.

---

## Updating the App

To get the latest changes from GitHub:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## Folder Structure

```
excel_chatbot/
├── ui/                      # User interfaces
│   ├── chatbot_byok_ui.py  # BYOK mode (user provides keys)
│   └── chatbot_upload_ui.py # Proxy mode (you provide key)
├── src/                     # Core functionality
│   ├── chatbot.py
│   ├── data_loader.py
│   ├── llm_provider.py
│   └── vector_store.py
├── requirements.txt         # Python packages
├── .env.example            # Example config
└── README.md               # Documentation
```

---

## Which Mode Should You Use?

### BYOK Mode (`chatbot_byok_ui.py`)
✅ Users provide their own API keys
✅ No cost to you
✅ Users choose their preferred AI (Claude, Gemini, GPT)
✅ Best for public/shared use

### Proxy Mode (`chatbot_upload_ui.py`)
✅ You provide the API key
✅ Users don't need accounts
✅ You control which AI is used
✅ Best for internal/controlled use
⚠️ You pay for all usage

---

## Getting Help

1. Check the error message in terminal
2. Read the troubleshooting section above
3. Search the error on Google/Stack Overflow
4. Check Python/Streamlit documentation

---

## Quick Reference Card

### First Time Setup
```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/excel_chatbot.git
cd excel_chatbot

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows)
venv\Scripts\activate

# 3. Activate (macOS/Linux)
source venv/bin/activate

# 4. Install packages
pip install -r requirements.txt

# 5. Run app
streamlit run ui/chatbot_byok_ui.py
```

### Every Time You Use It
```bash
cd excel_chatbot
venv\Scripts\activate              # Windows
source venv/bin/activate           # macOS/Linux
streamlit run ui/chatbot_byok_ui.py
```

---

## System Requirements

- **Python**: 3.10 or higher (3.11 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for dependencies
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Internet**: Required for downloading packages and API calls

---

**You're all set! 🚀**

Open http://localhost:8501 in your browser and start chatting with your Excel data!
