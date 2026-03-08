# AWS EC2 Setup - Step by Step

## 1. CREATE EC2 INSTANCE

### Go to AWS Console
1. Open: https://console.aws.amazon.com/ec2/
2. Click **"Launch Instances"** button

### Configure Instance
```
Instance name: ChurnGuard-Pro
Amazon Machine Image (AMI): Ubuntu Server 22.04 LTS (Free tier eligible)
Instance type: t2.micro (Free tier)
Key pair: 
  - Click "Create new key pair"
  - Name: churnguard-key
  - Type: RSA
  - Format: .pem (for Mac/Linux) or .ppk (for PuTTY on Windows)
  - Click "Create key pair"
  - FILE WILL DOWNLOAD - SAVE IT SECURELY!

Network settings:
  - VPC: Default VPC
  - Subnet: Default
  - Auto-assign public IP: Enable
  
Firewall (Security Group):
  - Create security group: churnguard-sg
  - Inbound rules (add these):
    1. Type: SSH, Port: 22, Source: My IP (YOUR_IP)
    2. Type: HTTP, Port: 80, Source: Anywhere (0.0.0.0/0)
    3. Type: HTTPS, Port: 443, Source: Anywhere (0.0.0.0/0)

Storage:
  - 30 GB (default is fine)

Cost estimate: FREE (12 months free tier)
```

### Launch
- Click **"Launch Instance"** button
- Wait 2-3 minutes for instance to start
- You should see green status "running"

---

## 2. GET YOUR SERVER IP

1. In EC2 Dashboard, click on your instance
2. Look for **Public IPv4 address** (e.g., `54.123.456.789`)
3. **SAVE THIS** - you'll need it for domain setup

---

## 3. CONNECT VIA SSH

### On Windows (PowerShell):
```powershell
# Navigate to where you downloaded key.pem
cd C:\Users\YourName\Downloads

# Set proper permissions
icacls churnguard-key.pem /grant:r "$($env:USERNAME):(F)"

# Connect to server
ssh -i churnguard-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# If it asks "Are you sure?" → Type: yes
```

### On Mac/Linux (Terminal):
```bash
# Navigate to key
cd ~/Downloads

# Set permissions
chmod 400 churnguard-key.pem

# Connect
ssh -i churnguard-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

You should now see a terminal prompt like: `ubuntu@ip-172-xx-xx-xx:~$`

---

## 4. CLONE YOUR APPLICATION

```bash
# On the EC2 instance (terminal):

# Go to home directory
cd /home/ubuntu

# Clone the repository
git clone https://github.com/YOUR_USERNAME/ChurnProject.git

# Navigate into it
cd ChurnProject

# Verify files are there
ls -la
# Should show: backend/, frontend/, docker-compose.yml, etc.
```

---

## 5. RUN THE QUICK DEPLOY SCRIPT

```bash
# Still on EC2 instance:

# Make script executable
chmod +x quick-deploy.sh

# Run deployment (replace with your actual domain and email)
bash quick-deploy.sh yourdomain.com your@email.com

# This will:
# - Install Docker
# - Install Docker Compose
# - Get SSL certificate
# - Configure Nginx
# - Start all services
# - Setup auto-renewal

# Takes about 5-10 minutes
```

---

## 6. POINT YOUR DOMAIN TO THE SERVER

### Add DNS Record

**If using Namecheap:**
```
1. Login to Namecheap
2. Dashboard → Manage Domain
3. Go to "Advanced DNS" tab
4. Find "Host Records" section
5. Add new record:
   - Type: A Record
   - Host: @
   - Value: YOUR_EC2_PUBLIC_IP (the one from step 2)
   - TTL: 30 min
6. Click Green checkmark
7. Click "Save all"
```

**If using GoDaddy:**
```
1. MyProducts → Domains
2. Select domain
3. DNS Management
4. Edit DNS Records
5. Find A Record with @
6. Change Value to: YOUR_EC2_PUBLIC_IP
7. Save
```

**If using Route 53 (AWS managed):**
```
1. AWS Console → Route 53
2. Hosted Zones → Create Hosted Zone
3. Domain name: yourdomain.com
4. Create
5. Create A record:
   - Name: yourdomain.com
   - Type: A
   - Value: YOUR_EC2_PUBLIC_IP
6. Create records
7. Copy nameservers (NS records)
8. Go to your domain registrar
9. Update nameservers to Route 53 ones
```

---

## 7. WAIT FOR DNS PROPAGATION

DNS changes take **5-10 minutes** to propagate globally.

Check status:
```bash
# Open command prompt/terminal on your local machine (NOT on EC2)

# Windows PowerShell:
nslookup yourdomain.com

# Mac/Linux:
nslookup yourdomain.com

# Should return YOUR_EC2_PUBLIC_IP

# Or use: https://www.whatsmydns.net
```

---

## 8. TEST YOUR DEPLOYMENT

After DNS propagates:

```
1. Open browser
2. Go to: https://yourdomain.com
3. Should see:
   - Indigo Airlines logo
   - ChurnGuard Pro title
   - Cinematic animations
   - "Built by Prabhmeet Singh Ahuja"
   - Full dashboard with charts
```

### If you see HTTPS lock 🔒
✅ Everything is working perfectly!

---

## 9. VERIFY API IS WORKING

```bash
# From your local machine terminal:

# Check API health
curl https://yourdomain.com/api/health

# Should return:
# {"status":"healthy","service":"ChurnGuard Pro API","version":"1.0.0"}
```

---

## TROUBLESHOOTING

### Can't SSH to instance?
- Check security group allows SSH (port 22) from your IP
- Verify key permissions: `chmod 400 key.pem`
- Check instance is running in AWS Console
- Copy-paste exact public IP (no typos)

### Domain not resolving?
- Check DNS record is correct (Type: A, Value: your IP)
- Wait another 5-10 minutes (DNS cache)
- Test: https://www.whatsmydns.net

### HTTPS not working?
- Check SSL certificate was created:
  ```bash
  sudo certbot certificates
  ```
- Check Nginx config:
  ```bash
  sudo nginx -t
  sudo systemctl status nginx
  ```

### Application pages blank?
- Check Docker running:
  ```bash
  docker ps
  ```
- View logs:
  ```bash
  docker compose logs -f
  ```

### Port 22 access denied?
In AWS Console:
1. Go to EC2 → Security Groups
2. Select churnguard-sg
3. Edit Inbound rules
4. SSH rule: Change Source to "My IP" (click "My IP" button)
5. Save

---

## MONITORING AFTER DEPLOYMENT

```bash
# SSH to your instance periodically to check:

# View all containers running
docker ps

# Check logs
docker compose logs -f

# Check health
curl https://yourdomain.com/api/health

# Check storage
df -h

# Check CPU/memory
free -h
```

---

## COST CHECK

**Your first 12 months:**
- EC2 t2.micro: FREE ✅
- 30GB storage: FREE ✅
- Data transfer: ~1GB free/month ✅
- SSL certificate: FREE ✅
- Domain: ~$8-15/year ✅

**Total: Essentially FREE (except domain)**

After 12 months, t2.micro costs ~$10/month if kept running.

---

## WHAT YOU'LL HAVE

✅ Your app running on `https://yourdomain.com`  
✅ Accessible worldwide  
✅ HTTPS secured  
✅ Auto SSL renewal  
✅ Production-ready  
✅ Scalable to thousands of users  

---

## QUICK COMMAND REFERENCE

```bash
# SSH to instance
ssh -i key.pem ubuntu@YOUR_EC2_IP

# Stop all services
docker compose stop

# Start all services
docker compose start

# View logs
docker compose logs -f

# Update app code
git pull origin main
docker compose up -d --build

# Check domain DNS
nslookup yourdomain.com

# Check SSL certificate
sudo certbot certificates
```

---

## NEXT STEPS

1. ✅ Create EC2 instance (follow steps 1-3 above)
2. ✅ Get your Public IPv4 address
3. ✅ Buy domain name or register free one
4. ✅ SSH to instance and clone ChurnProject
5. ✅ Run quick-deploy.sh with your domain
6. ✅ Add DNS record pointing to your IP
7. ✅ Wait for DNS to propagate
8. ✅ Visit `https://yourdomain.com` 🎉

---

Built by: Prabhmeet Singh Ahuja  
Platform: ChurnGuard Pro - Indigo Airlines Intelligence System
