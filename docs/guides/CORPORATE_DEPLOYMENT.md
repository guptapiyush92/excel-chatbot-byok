# Corporate Deployment Guide

Complete guide for deploying Excel Chatbot in firewall-protected corporate environments.

---

## 🎯 **Quick Decision Guide**

| Environment | Best Option | Complexity |
|-------------|-------------|------------|
| Small team (<20 users) | **Option 1: Direct Server** | ⭐ Easy |
| Medium team (20-100) | **Option 2: Docker** | ⭐⭐ Moderate |
| Enterprise (100+) | **Option 5: Kubernetes** | ⭐⭐⭐⭐ Advanced |
| Windows Server | **Option 4: IIS** | ⭐⭐⭐ Moderate |
| Need SSL/Domain | **Option 3: Nginx** | ⭐⭐ Moderate |

---

## 📋 **Pre-Deployment Checklist**

### Required:
- [ ] Linux/Windows server with Python 3.11+
- [ ] Network access from users to server
- [ ] Port 8000 (or custom) available
- [ ] 4GB RAM minimum (8GB recommended)
- [ ] 10GB disk space

### Optional (but recommended):
- [ ] Domain name (e.g., excel-chatbot.company.com)
- [ ] SSL certificate
- [ ] Backup strategy
- [ ] Monitoring solution

---

## 🚀 **Option 1: Direct Server Deployment (Recommended for Most)**

### **Best For:**
- Small to medium teams
- Quick setup needed
- Simple infrastructure

### **Step-by-Step:**

#### 1. **Setup Server**

```bash
# SSH into your server
ssh user@your-server.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y
```

#### 2. **Clone Repository**

```bash
# Navigate to application directory
cd /opt

# Clone repo
sudo git clone https://github.com/guptapiyush92/excel-chatbot-byok.git
cd excel-chatbot-byok

# Set permissions
sudo chown -R $USER:$USER /opt/excel-chatbot-byok
```

#### 3. **Install Dependencies**

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate
source venv/bin/activate

# Install
pip install --upgrade pip
pip install -r requirements-api.txt
```

#### 4. **Test Run**

```bash
# Test it works
cd /opt/excel-chatbot-byok
source venv/bin/activate
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Access from another machine: http://your-server-ip:8000
# If it works, proceed to make it permanent
```

#### 5. **Create Systemd Service**

```bash
# Create service file
sudo nano /etc/systemd/system/excel-chatbot.service
```

**Paste this (update paths):**

```ini
[Unit]
Description=Excel Chatbot FastAPI Application
After=network.target

[Service]
Type=simple
User=your-username
Group=your-username
WorkingDirectory=/opt/excel-chatbot-byok
Environment="PATH=/opt/excel-chatbot-byok/venv/bin"
ExecStart=/opt/excel-chatbot-byok/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable excel-chatbot

# Start now
sudo systemctl start excel-chatbot

# Check status
sudo systemctl status excel-chatbot

# View logs
sudo journalctl -u excel-chatbot -f
```

#### 6. **Configure Firewall**

```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Or restrict to specific network
sudo ufw allow from 10.0.0.0/8 to any port 8000

# Enable firewall
sudo ufw enable
```

#### 7. **Access**

Users access at: `http://your-server-hostname:8000`

**Done!** ✅

---

## 🐳 **Option 2: Docker Deployment**

### **Best For:**
- Teams familiar with Docker
- Need isolation
- Easy scaling

### **Step-by-Step:**

#### 1. **Install Docker**

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. **Clone and Build**

```bash
# Clone
git clone https://github.com/guptapiyush92/excel-chatbot-byok.git
cd excel-chatbot-byok

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

#### 3. **Access**

Users access at: `http://your-server-hostname:8000`

**Management commands:**

```bash
# Stop
docker-compose down

# Restart
docker-compose restart

# Update
git pull
docker-compose up -d --build

# View logs
docker-compose logs -f excel-chatbot
```

---

## 🌐 **Option 3: Nginx Reverse Proxy (Recommended for Production)**

### **Best For:**
- Production deployments
- Need SSL/HTTPS
- Want custom domain

### **Prerequisites:**
- Completed Option 1 or 2
- Domain name (optional)
- SSL certificate (optional)

### **Step-by-Step:**

#### 1. **Install Nginx**

```bash
sudo apt install nginx -y
```

#### 2. **Configure Nginx**

```bash
# Copy provided config
sudo cp nginx.conf /etc/nginx/sites-available/excel-chatbot

# Edit with your domain
sudo nano /etc/nginx/sites-available/excel-chatbot

# Update this line:
# server_name excel-chatbot.yourcompany.com;

# Enable site
sudo ln -s /etc/nginx/sites-available/excel-chatbot /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

#### 3. **Setup SSL (Optional but Recommended)**

**Using Let's Encrypt (Free):**

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d excel-chatbot.yourcompany.com

# Auto-renewal is setup automatically
```

**Using Corporate Certificate:**

```bash
# Place certificates
sudo cp your-cert.crt /etc/ssl/certs/excel-chatbot.crt
sudo cp your-key.key /etc/ssl/private/excel-chatbot.key

# Update nginx config to use them
```

#### 4. **Access**

Users access at: `https://excel-chatbot.yourcompany.com`

---

## 🪟 **Option 4: Windows Server (IIS)**

### **Best For:**
- Windows-only environments
- IIS infrastructure already in place

### **Step-by-Step:**

#### 1. **Install Prerequisites**

- Python 3.11 from python.org
- IIS with HttpPlatformHandler module
- Git for Windows

#### 2. **Clone and Setup**

```powershell
# Clone
cd C:\inetpub\
git clone https://github.com/guptapiyush92/excel-chatbot-byok.git
cd excel-chatbot-byok

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install
pip install -r requirements-api.txt
```

#### 3. **Configure IIS**

1. Open IIS Manager
2. Add new site:
   - Site name: ExcelChatbot
   - Physical path: `C:\inetpub\excel-chatbot-byok`
   - Binding: Port 80 or 443
3. Copy `web.config` to site root
4. Edit `web.config` with correct paths
5. Start site

#### 4. **Access**

Users access at: `http://your-server-name/`

---

## ☸️ **Option 5: Kubernetes (Enterprise)**

### **Best For:**
- Large enterprises
- Need high availability
- Auto-scaling requirements

### **Step-by-Step:**

#### 1. **Build Container**

```bash
# Build image
docker build -t your-registry.com/excel-chatbot:v1.0 .

# Push to registry
docker push your-registry.com/excel-chatbot:v1.0
```

#### 2. **Deploy to Kubernetes**

```bash
# Update kubernetes.yaml with your image
nano kubernetes.yaml

# Apply
kubectl apply -f kubernetes.yaml

# Check status
kubectl get pods
kubectl get services
kubectl get ingress
```

#### 3. **Access**

Users access via configured ingress URL.

---

## 🔒 **Security Hardening**

### 1. **Enable Authentication (Optional)**

Add authentication layer using:
- Corporate SSO (SAML/OAuth)
- Basic Auth via Nginx
- API Key validation

### 2. **Network Security**

```bash
# Restrict to corporate network
sudo ufw allow from 10.0.0.0/8 to any port 8000

# Or use VPN requirement
```

### 3. **Rate Limiting**

Add to nginx config:

```nginx
limit_req_zone $binary_remote_addr zone=chatbot_limit:10m rate=10r/s;

server {
    location / {
        limit_req zone=chatbot_limit burst=20;
        ...
    }
}
```

### 4. **File Size Limits**

Already configured (50MB default). Adjust in:
- nginx.conf: `client_max_body_size`
- api/main.py: `MAX_UPLOAD_SIZE`

---

## 📊 **Monitoring**

### **Check Application Health**

```bash
curl http://localhost:8000/api/health
```

### **View Logs**

**Systemd:**
```bash
sudo journalctl -u excel-chatbot -f
```

**Docker:**
```bash
docker-compose logs -f
```

**Kubernetes:**
```bash
kubectl logs -f deployment/excel-chatbot
```

### **Monitoring Tools**

- **Prometheus + Grafana** - Metrics
- **ELK Stack** - Log aggregation
- **Uptime Robot** - Availability monitoring

---

## 🔄 **Updates and Maintenance**

### **Update Application**

**Systemd:**
```bash
cd /opt/excel-chatbot-byok
git pull
source venv/bin/activate
pip install -r requirements-api.txt --upgrade
sudo systemctl restart excel-chatbot
```

**Docker:**
```bash
cd /path/to/excel-chatbot-byok
git pull
docker-compose up -d --build
```

**Kubernetes:**
```bash
docker build -t your-registry.com/excel-chatbot:v1.1 .
docker push your-registry.com/excel-chatbot:v1.1
kubectl set image deployment/excel-chatbot excel-chatbot=your-registry.com/excel-chatbot:v1.1
```

---

## 🆘 **Troubleshooting**

### **Application Won't Start**

```bash
# Check logs
sudo journalctl -u excel-chatbot -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000

# Test manually
source venv/bin/activate
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### **Can't Access from Other Machines**

```bash
# Check firewall
sudo ufw status

# Check if listening
sudo netstat -tulpn | grep 8000

# Should show 0.0.0.0:8000, not 127.0.0.1:8000
```

### **High Memory Usage**

```bash
# Reduce workers
# In systemd service or docker-compose, change:
--workers 4  # to  --workers 2
```

---

## 📋 **Post-Deployment Checklist**

- [ ] Application accessible from user machines
- [ ] SSL certificate installed (if using HTTPS)
- [ ] Firewall rules configured
- [ ] Monitoring setup
- [ ] Backup strategy defined
- [ ] Users trained on access URL
- [ ] API proxy configured (if needed)
- [ ] Log rotation setup
- [ ] Update procedure documented

---

## 🎯 **Recommended Setup for Most Companies**

**Small Company (<50 users):**
- Option 1 (Direct Server)
- With Option 3 (Nginx + SSL)
- Total time: 1-2 hours

**Medium Company (50-500 users):**
- Option 2 (Docker)
- With Option 3 (Nginx + SSL)
- Add monitoring
- Total time: 2-4 hours

**Large Enterprise (500+ users):**
- Option 5 (Kubernetes)
- With Ingress + SSL
- Full monitoring stack
- Total time: 1-2 days

---

## 📞 **Getting Help**

**Before contacting IT:**
- Document exact error messages
- Check application logs
- Verify firewall rules
- Test from different machines

**Provide IT with:**
- Port requirements (8000 or custom)
- Network access needs
- SSL certificate requirements
- Domain name requirements

---

**Your Excel Chatbot is ready for corporate deployment!** 🚀

Choose the option that fits your infrastructure and follow the guide.
