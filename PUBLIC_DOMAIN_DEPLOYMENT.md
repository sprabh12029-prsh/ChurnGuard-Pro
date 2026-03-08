# ChurnGuard Pro - Public Domain Deployment Guide

## 🚀 Deploy on Public Domain (AWS + Custom Domain)

This guide will help you deploy ChurnGuard Pro on a public domain accessible worldwide.

---

## **STEP 1: Prepare Your Domain**

### Option A: Buy Domain (Recommended)
1. Go to **Namecheap** (https://namecheap.com), **GoDaddy**, or any registrar
2. Search for your domain (e.g., `churnguard.com`)
3. Purchase the domain (typically $8-15/year)
4. Get your domain name (e.g., `yourdomain.com`)

### Option B: Use Free Domain
- Use **Freenom** (https://www.freenom.com) for free `.ml`, `.tk` domains
- Or use AWS Route 53 subdomain (automatically included)

---

## **STEP 2: Create AWS EC2 Instance**

### A. Create EC2 Instance
```bash
1. Go to AWS Console: https://console.aws.amazon.com
2. EC2 → Instances → Launch Instances
3. Select: Ubuntu Server 22.04 LTS (Free tier eligible)
4. Instance Type: t2.micro (Free tier)
5. Key Pair: Create new → Save .pem file securely
6. Security Group: 
   - Add HTTP (80)
   - Add HTTPS (443)
   - Add SSH (22)
7. Storage: 30GB (default ok)
8. Launch Instance
```

### B. Connect to Instance
```bash
# On Windows (PowerShell):
cd C:\path\to\your\key.pem
# Set permissions
icacls key.pem /grant:r "$($env:USERNAME):(F)"

# SSH Connection:
ssh -i key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## **STEP 3: Deploy Application on EC2**

### A. Clone Your Repository
```bash
# On EC2 instance:
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/ChurnProject.git
cd ChurnProject
```

### B. Run Deployment Script
```bash
# Make script executable
chmod +x deploy-aws.sh

# Run deployment (automated)
bash deploy-aws.sh
```

### C. Manual Deployment (if script fails)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start services
cd ChurnProject
docker compose up -d --build
```

---

## **STEP 4: Configure Your Domain**

### A. Get Your EC2 Public IP
```bash
# On AWS Console:
EC2 → Instances → Select your instance → Copy Public IPv4 address
# e.g., 54.123.456.789
```

### B. Point Domain to EC2 (via Domain Registrar)

**For Namecheap:**
```
1. Login to Namecheap
2. Dashboard → Manage Domain
3. Advanced DNS Tab
4. Host Records:
   - Type: A Record
   - Host: @ (root)
   - Value: YOUR_EC2_PUBLIC_IP
   - TTL: 30 min
5. Save changes
```

**For GoDaddy:**
```
1. MyProducts → Domains
2. DNS Management
3. Edit A Record:
   - @ → YOUR_EC2_PUBLIC_IP
   - www → YOUR_EC2_PUBLIC_IP
```

**For AWS Route 53:**
```
1. Route 53 → Hosted Zones
2. Create new hosted zone (yourdomain.com)
3. Create A Record:
   - Name: yourdomain.com
   - Type: A
   - Value: YOUR_EC2_PUBLIC_IP
4. Update domain registrar nameservers to Route 53 nameservers
```

---

## **STEP 5: Setup SSL Certificate (FREE)**

### Using Let's Encrypt with Certbot
```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL Certificate
sudo certbot certonly --standalone \
    -d yourdomain.com \
    -d www.yourdomain.com \
    --email your@email.com \
    --agree-tos \
    --non-interactive

# Certificates saved to:
# /etc/letsencrypt/live/yourdomain.com/
```

---

## **STEP 6: Configure Nginx for HTTPS**

### Update Nginx Config
```bash
# SSH into EC2
ssh -i key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Edit nginx config
sudo nano frontend/nginx.conf
```

**Add this:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

### Restart Services
```bash
docker compose restart
```

---

## **STEP 7: Verify Deployment**

### Test Your Domain
```
1. Open browser: https://yourdomain.com
2. Should see ChurnGuard Pro dashboard with:
   - Indigo logo
   - Cinematic animations
   - "Built by Prabhmeet Singh Ahuja"
   - All interactive features
```

### Check API Health
```bash
curl https://yourdomain.com/api/health

# Should return:
# {"status":"healthy","service":"ChurnGuard Pro API","version":"1.0.0"}
```

### Monitor Logs
```bash
# Docker logs
docker compose logs -f backend
docker compose logs -f frontend

# Application health
curl https://yourdomain.com/api/status
```

---

## **STEP 8: Auto-Renew SSL (Recommended)**

```bash
# Create renewal script
sudo tee /usr/local/bin/renew-ssl.sh > /dev/null <<EOF
#!/bin/bash
certbot renew --quiet
docker compose restart frontend
EOF

# Make executable
sudo chmod +x /usr/local/bin/renew-ssl.sh

# Add to cron (auto-renew every 60 days)
sudo crontab -e

# Add this line:
0 0 1 * * /usr/local/bin/renew-ssl.sh
```

---

## **QUICK REFERENCE - ONE-LINER DEPLOYMENT**

After domain setup:

```bash
# On EC2 Instance:
git clone https://github.com/YOUR_USERNAME/ChurnProject.git && \
cd ChurnProject && \
chmod +x deploy-aws.sh && \
bash deploy-aws.sh
```

---

## **COST ESTIMATE**

| Item | Cost | Notes |
|------|------|-------|
| Domain | $8-15/year | One-time yearly |
| AWS EC2 t2.micro | FREE | First 12 months free tier eligible |
| SSL Certificate | FREE | Let's Encrypt (auto-renew) |
| **TOTAL** | **$0-15/year** | Completely free for first year! |

---

## **TROUBLESHOOTING**

### Domain not resolving
```bash
# Check DNS propagation
nslookup yourdomain.com
# or use: https://www.whatsmydns.net
```

### SSL certificate errors
```bash
# Verify certificate
sudo certbot certificates

# Force renewal
sudo certbot renew --force-renewal
```

### Services not running
```bash
# Check Docker status
docker ps -a

# View logs
docker compose logs

# Restart all services
docker compose restart
```

### Can't connect via SSH
1. Check security group allows SSH (port 22)
2. Check key.pem permissions: `chmod 400 key.pem`
3. Verify public IP and instance running

---

## **NEXT STEPS AFTER DEPLOYMENT**

1. ✅ Test at: `https://yourdomain.com`
2. ✅ Share with anyone globally
3. ✅ Monitor via CloudWatch
4. ✅ Setup email alerts
5. ✅ Configure backups

---

## **SUPPORT**

For issues:
- AWS Support: https://console.aws.amazon.com/support
- Let's Encrypt: https://community.letsencrypt.org
- Docker: https://docs.docker.com

**Built by:** Prabhmeet Singh Ahuja  
**Platform:** ChurnGuard Pro - Indigo Airlines Intelligence System
