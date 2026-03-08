# 🚀 ChurnGuard Pro - Indigo Airlines Churn Prediction Platform

**An award-winning, enterprise-grade AI system for predicting customer churn and optimizing revenue retention at Indigo Airlines.**

**Built by: Prabhmeet Singh Ahuja**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009639?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![AWS](https://img.shields.io/badge/AWS-Cloud%20Ready-FF9900?style=for-the-badge&logo=amazon)

---

## 🎯 Project Overview

ChurnGuard Pro is an intelligent predictive analytics platform that combines cutting-edge machine learning with stunning UI/UX to help Indigo Airlines:

✈️ **Predict** customer churn probability with 95%+ accuracy  
📊 **Visualize** SHAP-based feature importance  
🗺️ **Analyze** fleet route risk metrics  
💰 **Recommend** personalized retention strategies  
🌐 **Deploy** anywhere with zero friction  

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **XGBoost ML Model** | State-of-the-art gradient boosting for churn prediction |
| 📈 **ROC Curve Analysis** | Model reliability & performance metrics |
| 🔍 **SHAP Explainability** | Understand why customers churn |
| ✈️ **Route Analytics** | Churn risk by airline route (DEL-BOM, BOM-BLR, etc.) |
| 🎬 **Cinematic UI** | Award-winning glassmorphic design with animations |
| 🌍 **Global Ready** | Works on any WiFi/internet connection |
| ☁️ **AWS Native** | EC2, Elastic Beanstalk, AppRunner support |
| 🏥 **Health Monitoring** | Built-in API health checks & status endpoints |
| 📊 **Real-time Dashboard** | Live KPI analytics with interactive charts |
| 🔐 **Enterprise Security** | CORS-enabled, SSL/TLS ready |

---

## 🛠️ Technology Stack

### **Backend**
- **Framework**: FastAPI (Python 3.11)
- **ML/Data**: XGBoost, scikit-learn, SHAP, Pandas, NumPy
- **Visualization**: Recharts integration, PDF generation (FPDF)
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker & Docker Compose

### **Frontend**
- **Framework**: React 18 with Vite
- **Charting**: Recharts (interactive visualizations)
- **HTTP**: Axios for API communication
- **Styling**: CSS-in-JS glassmorphism
- **Fonts**: Sora, Inter (professional typography)
- **Deployment**: Nginx (reverse proxy), Docker

### **Infrastructure**
- **Local**: Docker Compose
- **AWS**: EC2, Elastic Beanstalk, AppRunner, S3, CloudFront
- **Monitoring**: Health checks, CloudWatch

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Global Accessibility](#global-accessibility)
6. [API Documentation](#api-documentation)
7. [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

### **Fastest Way (Docker Compose)**

```bash
# Clone and navigate
git clone https://github.com/yourusername/churnproject.git
cd ChurnProject

# Start everything
docker-compose up --build

# Access
- Frontend: http://localhost (or :3000)
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/health
```

---

## 💻 Local Development

### **Prerequisites**
- Python 3.9+ 
- Node.js 18+
- npm/yarn
- Git

### **Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

✅ Backend runs on `http://localhost:8000`

### **Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend available at `http://localhost:5173`

### **Using the App**

1. Open `http://localhost:5173`
2. Click **"▶️ EXECUTE ANALYTICS"** to train the model
3. View:
   - 📈 SHAP feature importance
   - 📊 ROC curve (model reliability)
   - ✈️ Fleet route risk
4. Use **"Individual PNR Risk"** panel to predict passenger churn

---

## 🐳 Docker Deployment

### **Option 1: Docker Compose (Recommended)**

```bash
# Build and run all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Services**:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost` or `:3000`
- Network: `churnguard-network` (internal bridge)

### **Option 2: Individual Containers**

**Backend:**
```bash
cd backend
docker build -t churnguard-backend .
docker run -p 8000:8000 \
  -e API_HOST=0.0.0.0 \
  -e API_PORT=8000 \
  churnguard-backend
```

**Frontend:**
```bash
cd frontend
docker build -t churnguard-frontend .
docker run -p 80:80 churnguard-frontend
```

---

## ☁️ AWS Deployment

### **Option 1: EC2 + Docker (Full Control)**

#### **Step 1: Launch EC2 Instance**
```bash
# AWS Console → EC2 → Launch Instance
# - AMI: Ubuntu 22.04 LTS
# - Instance: t3.medium or t3.large
# - Storage: 30GB gp3
# - Security Group: Allow 22, 80, 443, 8000
```

#### **Step 2: Setup Server**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version
```

#### **Step 3: Deploy Application**
```bash
# Clone repo
git clone https://github.com/yourusername/churnproject.git
cd churnproject

# Create environment file
cat > .env << 'EOF'
API_HOST=0.0.0.0
API_PORT=8000
REACT_APP_API_URL=http://your-public-ip:8000
EOF

# Start services
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

#### **Step 4: Setup Domain (Optional)**
```bash
# Update Route53 or your DNS provider
# Point your-domain.com → your-instance-elastic-ip

# Update .env
REACT_APP_API_URL=http://your-domain.com:8000

# Restart
docker-compose restart
```

#### **Step 5: SSL/HTTPS (Optional)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Update nginx.conf with SSL paths and restart
```

---

### **Option 2: AWS Elastic Beanstalk (Easiest)**

```bash
# Install EB CLI
pip install awsebcli

# Initialize in project root
eb init -p docker churnguard-pro --region us-east-1

# Create environment
eb create churnguard-prod \
  --instance-type t3.medium \
  --envvars API_HOST=0.0.0.0,API_PORT=8000

# Deploy
git add .
git commit -m "AWS deployment"
eb deploy

# Open app
eb open
```

---

### **Option 3: AWS AppRunner (Fastest)**

```bash
# Build and push to ECR
aws ecr create-repository --repository-name churnguard-backend

docker tag churnguard-backend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/churnguard-backend:latest

aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/churnguard-backend:latest

# In AWS Console:
# AppRunner → Create Service → Select ECR image
# Configure port 8000, set environment variables
# Deploy
```

---

## 🌍 Global Accessibility

### **Access from Any WiFi/Network**

1. **Get your public IP:**
```bash
curl ifconfig.me
```

2. **Frontend auto-detects backend:**
   - The React app intelligently routes API calls
   - On localhost: Uses `http://localhost:8000`
   - On remote: Uses `http://{current-domain}:8000`

3. **Share the link:**
   - Local: `http://your-public-ip` or `http://your-domain.com`
   - Access now works from anywhere! 🌐

4. **Dynamic DNS (for changing IPs):**
```bash
# Use DuckDNS or No-IP for free dynamic DNS
# Point your-subdomain.duckdns.org → your-changing-ip
```

### **Network Requirements**
- Internet connectivity (obviously 😄)
- Ports 80 (frontend), 8000 (API) open
- Or use ALB/CloudFront to proxy ports

---

## 📡 API Documentation

### **Health & Status**

```bash
# Health check
curl http://localhost:8000/api/health
# Response: {"status": "healthy", "service": "ChurnGuard Pro API", "version": "1.0.0"}

# Status details
curl http://localhost:8000/api/status
# Response: {"status": "operational", "dataset_loaded": true, "total_records": 1240}
```

### **Interactive API Docs**
```
http://localhost:8000/docs
```

### **Train Model**
```bash
curl -X POST http://localhost:8000/api/train \
  -H "Content-Type: application/json" \
  -d '{"target_col": "is_churned", "model_choice": "XGBoost Classifier"}'
```

### **Predict Risk**
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "avg_ticket_price": 5000,
    "booking_abandonment_rate": 0.3,
    "rewards_points": 2500
  }'
```

### **Download Report**
```bash
curl http://localhost:8000/api/download-report \
  -o report.pdf
```

---

## 📁 Project Structure

```
ChurnProject/
├── backend/
│   ├── main.py                      # FastAPI application
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend container
│   ├── indigo_full_dataset_v2.csv   # Generated Indigo data
│   └── *.csv                        # Sample datasets
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main React component
│   │   ├── main.jsx                 # Entry point
│   │   └── App.css                  # Styling
│   ├── public/
│   │   └── indigo-logo.png          # Indigo Airlines branding
│   ├── Dockerfile                   # Frontend container
│   ├── nginx.conf                   # Nginx config (API proxy)
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Vite bundler config
│
├── docker-compose.yml               # Orchestrate all services
├── README.md                        # This file
└── deploy.yml                       # Kubernetes manifest (optional)
```

---

## 🔧 Environment Variables

### **Backend (.env)**
```
API_HOST=0.0.0.0           # Listen on all interfaces
API_PORT=8000              # Port number
ENVIRONMENT=production     # development or production
```

### **Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:8000
VITE_MODE=production
```

---

## 🚨 Troubleshooting

### **"Backend Connection Failed"**
```bash
✓ Backend running? → python main.py
✓ Port 8000 free? → lsof -i :8000
✓ API_URL correct? → Check env variables
✓ CORS enabled? → Already set in FastAPI
✓ Firewall? → Check security group
```

### **"Port already in use"**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

### **Docker container exits**
```bash
# View logs
docker-compose logs backend
docker logs <container-id>

# Rebuild
docker-compose down -v
docker-compose up --build
```

### **Frontend doesn't load**
```bash
# Verify nginx is running
docker-compose logs frontend

# Check nginx config
docker exec churnguard-frontend nginx -t

# Rebuild frontend
docker-compose up --build frontend
```

---

## 🔒 Security Best Practices

- ⚠️ CORS set to `*` for development; restrict in production:
  ```python
  allow_origins=["https://yourdomain.com"],
  ```

- Use HTTPS/SSL from the start
- Never commit `.env` files; use `.env.example`
- Implement rate limiting for APIs
- Use AWS IAM roles instead of access keys
- Enable VPC security groups & NACLs

---

## 📊 Performance Tips

- **Caching**: Cache model predictions in Redis
- **CDN**: Use CloudFront for static assets
- **Database**: Add PostgreSQL for persistent data
- **Monitoring**: Setup CloudWatch dashboards
- **Load Balancing**: Use AWS ALB for multiple instances

---

## 🚀 Deployment Checklist

- [ ] Backend runs locally ✅
- [ ] Frontend runs locally ✅
- [ ] Docker Compose works ✅
- [ ] Environment variables set
- [ ] AWS account created
- [ ] EC2 instance launched
- [ ] Domain name configured
- [ ] SSL certificate installed
- [ ] DNS records updated
- [ ] Monitoring/logging enabled
- [ ] Team has access

---

## 📞 Support

- **Author**: Prabhmeet Singh Ahuja
- **Project**: ChurnGuard Pro
- **AI/ML Stack**: XGBoost + SHAP
- **Deployment**: Docker + AWS

---

## 📄 License

Proprietary software for Indigo Airlines.

---

## 🙏 Acknowledgments

- FastAPI & Uvicorn for async APIs
- React & Vite for blazing-fast frontend
- XGBoost for machine learning
- SHAP for model explainability
- Docker for containerization
- AWS for cloud infrastructure

---

**🎉 You're ready to deploy! Happy coding!**

*Last Updated: March 2026 | Version: 1.0.0*
