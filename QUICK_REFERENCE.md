# Quick Reference - ChurnGuard Pro Deployment Commands

## 🚀 Local Development

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

## 🐳 Docker Compose (Recommended for Production-like testing)

```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up --build backend
docker-compose up --build frontend
```

## ☁️ AWS EC2 Quick Deploy

```bash
# On AWS EC2 Instance (Ubuntu 22.04)
git clone https://github.com/yourusername/churnproject.git
cd churnproject
chmod +x deploy-aws.sh
./deploy-aws.sh

# Application will be automatically deployed and running
```

## 🌐 Access Points

| Component | Local | Docker | AWS |
|-----------|-------|--------|-----|
| Frontend | http://localhost:5173 | http://localhost | http://your-instance-ip |
| Backend API | http://localhost:8000 | http://localhost:8000 | http://your-instance-ip:8000 |
| API Docs | http://localhost:8000/docs | http://localhost:8000/docs | http://your-instance-ip:8000/docs |
| Health | http://localhost:8000/api/health | http://localhost:8000/api/health | http://your-instance-ip:8000/api/health |

## 🔧 Common Commands

```bash
# Build frontend
cd frontend && npm run build

# Health check
curl http://localhost:8000/api/health

# Check container status
docker-compose ps

# View specific logs
docker logs <container-id>

# Stop all services
docker-compose down

# Remove all containers and volumes
docker-compose down -v

# SSH to AWS instance
ssh -i your-key.pem ubuntu@your-instance-ip

# View AWS instance info
aws ec2 describe-instances --region us-east-1

# Get public IP
curl ifconfig.me
```

## 📦 Files Generated

- ✓ `docker-compose.yml` - Orchestration
- ✓ `backend/Dockerfile` - Backend container
- ✓ `frontend/Dockerfile` - Frontend container
- ✓ `frontend/nginx.conf` - Reverse proxy config
- ✓ `.env.example` - Environment template
- ✓ `.gitignore` - Git ignore rules
- ✓ `deploy-aws.sh` - Auto deployment script
- ✓ `README.md` - Full documentation
- ✓ `AWS_DEPLOYMENT_GUIDE.md` - AWS guide

## 🔐 Security Checklist

- [ ] Update CORS in backend/main.py for production domains
- [ ] Enable HTTPS/SSL with Let's Encrypt
- [ ] Restrict SSH access in Security Group
- [ ] Use strong passwords/key pairs
- [ ] Enable Cloudwatch monitoring
- [ ] Configure backup strategy
- [ ] Test disaster recovery

## 💰 Cost Estimate (AWS)

| Resource | Type | Est. Monthly |
|----------|------|------------|
| EC2 | t3.medium | $30 |
| Data Transfer | Outbound | $10 |
| Domain | Optional | $12 |
| **Total** | | **$40-52** |

## 🚨 Troubleshooting Quick Fixes

```bash
# Port already in use
lsof -i :8000
kill -9 <PID>

# Docker container won't start
docker-compose logs backend

# Rebuild everything
docker-compose down -v
docker-compose up --build

# Update application
git pull origin main
docker-compose up -d --build

# Check if backend is responding
curl http://localhost:8000/api/health

# View all environment variables
docker-compose config
```

## 📊 Performance Monitoring

```bash
# Backend monitoring
watch -n 1 'curl -s http://localhost:8000/api/health | python3 -m json.tool'

# Container resource usage
docker stats

# System resources
df -h      # Disk
free -h    # Memory
top        # CPU
```

## 🎯 Deployment Checklist

- [ ] Clone repository
- [ ] Create .env file
- [ ] Test locally (npm run dev + python main.py)
- [ ] Build Docker images (docker-compose up --build)
- [ ] Verify health checks
- [ ] Deploy to AWS
- [ ] Configure domain
- [ ] Enable SSL
- [ ] Test from external network
- [ ] Monitor logs
- [ ] Setup auto-restart
- [ ] Document access credentials
- [ ] Brief team

---

**For detailed guides, see:**
- README.md - Full project documentation
- AWS_DEPLOYMENT_GUIDE.md - Comprehensive AWS setup

**Build by**: Prabhmeet Singh Ahuja  
**Last Updated**: March 2026
