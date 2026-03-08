# AWS Deployment Guide - ChurnGuard Pro

## Complete Step-by-Step Amazon Web Services Deployment

**Author**: Prabhmeet Singh Ahuja  
**Date**: March 2026  
**Version**: 1.0.0

---

## 📋 Pre-Deployment Checklist

- [ ] AWS Account created and verified
- [ ] AWS CLI installed locally
- [ ] Docker & Docker Compose installed
- [ ] Git installed
- [ ] SSH key pair created in AWS
- [ ] GitHub repository ready
- [ ] Domain name (optional but recommended)

---

## 🚀 Quick Deploy (5 Minutes)

### **The Fastest Way: Run Deploy Script on EC2**

1. **Launch EC2 Instance**
   - AWS Console → EC2 → Launch Instance
   - Select: **Ubuntu 22.04 LTS**
   - Instance Type: **t3.medium** (or t3.large for higher traffic)
   - Storage: **30GB gp3**
   - Security Group: Allow SSH (22), HTTP (80), HTTPS (443), Custom TCP (8000)

2. **Connect & Deploy**
   ```bash
   # SSH into your instance
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Clone and run deployment
   git clone https://github.com/yourusername/churnproject.git
   cd churnproject
   
   # Make script executable and run
   chmod +x deploy-aws.sh
   ./deploy-aws.sh
   ```

3. **Done!** 🎉
   - Frontend: `http://your-instance-ip`
   - Backend: `http://your-instance-ip:8000`
   - API Docs: `http://your-instance-ip:8000/docs`

---

## 🏗️ Detailed Setup (Manual Method)

### **Step 1: Launch EC2 Instance**

```bash
# AWS CLI command to launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-groups churnguard-sg \
  --region us-east-1 \
  --ebs-optimized \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ChurnGuard-Pro}]'
```

### **Step 2: Configure Security Group**

```bash
# Create security group
aws ec2 create-security-group \
  --group-name churnguard-sg \
  --description "ChurnGuard Pro security group"

# Allow SSH (22)
aws ec2 authorize-security-group-ingress \
  --group-name churnguard-sg \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Allow HTTP (80)
aws ec2 authorize-security-group-ingress \
  --group-name churnguard-sg \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Allow HTTPS (443)
aws ec2 authorize-security-group-ingress \
  --group-name churnguard-sg \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Allow Backend API (8000)
aws ec2 authorize-security-group-ingress \
  --group-name churnguard-sg \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0
```

### **Step 3: SSH and Install Docker**

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L \
  "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### **Step 4: Deploy Application**

```bash
# Clone repository
git clone https://github.com/yourusername/churnproject.git
cd churnproject

# Create .env file
cat > .env << 'EOF'
API_HOST=0.0.0.0
API_PORT=8000
REACT_APP_API_URL=http://your-instance-public-ip:8000
ENVIRONMENT=production
EOF

# Start services
docker-compose up -d --build

# Wait for services to start
sleep 15

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### **Step 5: Verify Deployment**

```bash
# Health check
curl http://localhost:8000/api/health

# Status
curl http://localhost:8000/api/status

# Frontend (wait for response)
curl http://localhost | head -20
```

---

## 🌐 Setup Domain Name (Optional)

### **Using Route53**

```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name your-domain.com \
  --caller-reference $(date +%s)

# Create A record pointing to Elastic IP
# Get your Elastic IP first
aws ec2 describe-addresses --query 'Addresses[*].[PublicIp]' --output text

# Then create DNS record in Route53 Console
```

### **Update .env with Domain**

```bash
# SSH to instance
ssh -i your-key.pem ubuntu@your-instance-public-ip

# Update .env
cd churnproject
sed -i "s|http://.*:8000|http://your-domain.com:8000|g" .env

# Restart services
docker-compose restart
```

---

## 🔒 Enable HTTPS/SSL

### **Free SSL with Let's Encrypt**

```bash
# SSH to instance
ssh -i your-key.pem ubuntu@your-instance-public-ip

# Install Certbot
sudo apt install certbot -y

# Generate certificate
sudo certbot certonly --standalone \
  -d your-domain.com \
  -d www.your-domain.com

# Copy certificates to nginx
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ~/churnproject/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ~/churnproject/

# Update nginx.conf with SSL paths
# See: frontend/nginx.conf for SSL configuration example

# Restart services
docker-compose restart frontend
```

---

## 📊 Monitoring & Maintenance

### **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### **Restart Services**
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### **Stop/Start Services**
```bash
# Stop
docker-compose down

# Start again
docker-compose up -d
```

### **Update Application**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```

---

## 🔐 Security Best Practices

1. **Update Security Group**
   ```bash
   # Restrict SSH to your IP
   aws ec2 authorize-security-group-ingress \
     --group-name churnguard-sg \
     --protocol tcp \
     --port 22 \
     --cidr YOUR_IP/32
   ```

2. **Enable Automatic Updates**
   ```bash
   sudo apt install unattended-upgrades -y
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

3. **Firewall Configuration**
   ```bash
   sudo ufw enable
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw allow 8000
   ```

4. **Update Backend CORS for Production**
   ```python
   # In backend/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-domain.com", "https://www.your-domain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## 💰 Cost Optimization

| Component | Instance | Monthly Cost |
|-----------|----------|--------------|
| EC2 | t3.medium | ~$30 |
| Data Transfer | 100GB | ~$10 |
| Elastic IP | 1 | Free (if used) |
| **Total** | | **~$40/month** |

### **Tips to Reduce Costs**
- Use **t3.micro** for low traffic (Free Tier eligible)
- Enable **auto-scaling** to reduce idle capacity
- Use **AWS Lambda + API Gateway** for event-driven workloads
- Cache responses with **CloudFront**

---

## 🆘 Troubleshooting

### **Cannot SSH**
```bash
# Check security group
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupName,IpPermissions]'

# Check instance status
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State]'
```

### **Docker Daemon Failed**
```bash
sudo service docker start
sudo service docker status
```

### **Out of Disk Space**
```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a
```

### **Application Not Responding**
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs

# Restart
docker-compose restart
```

---

## 📈 Scaling for Production

### **Option 1: Load Balancer (AWS ALB)**
```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name churnguard-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx
```

### **Option 2: Auto Scaling Group**
```bash
# Create AMI from current instance
aws ec2 create-image \
  --instance-id i-xxx \
  --name churnguard-ami

# Create launch template
aws ec2 create-launch-template \
  --launch-template-name churnguard-template \
  --version-description "v1" \
  --launch-template-data '{"ImageId":"ami-xxx","InstanceType":"t3.medium"}'

# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name churnguard-asg \
  --launch-template LaunchTemplateName=churnguard-template
```

### **Option 3: Elastic Beanstalk**
See README.md → AWS Deployment → Option 2

---

## 🎯 Next Steps

1. ✅ Deploy application
2. ✅ Setup domain name
3. ✅ Enable HTTPS
4. ✅ Configure monitoring
5. ✅ Setup backups
6. ✅ Load testing
7. ✅ Go live! 🚀

---

## 📞 Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- View API docs: `http://your-domain:8000/docs`
- Review AWS CloudWatch metrics

---

**Happy Deploying! 🎉**

*ChurnGuard Pro - Built by Prabhmeet Singh Ahuja*
