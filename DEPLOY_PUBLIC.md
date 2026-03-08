# 🚀 ChurnGuard Pro - PUBLIC DOMAIN DEPLOYMENT SUMMARY

## Three Deployment Paths (Pick One)

---

## **PATH 1: FASTEST (5 minutes) - One Command Deploy ⚡**

### Requirements:
- AWS Account (free tier eligible)
- Domain name (e.g., from Namecheap $8/year)
- SSH key file (.pem)

### Steps:

**1. Create AWS EC2 Instance**
```
1. AWS Console → EC2 → Launch Instance
2. Select: Ubuntu 22.04 LTS (Free tier)
3. Instance Type: t2.micro
4. Create new key pair → download .pem file
5. Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
6. Launch instance
7. Copy Public IPv4 address
```

**2. Connect to Instance**
```bash
# PowerShell/Terminal
ssh -i path/to/key.pem ubuntu@YOUR_EC2_IP
```

**3. Deploy (One Command)**
```bash
# On EC2 instance:
curl -O https://raw.githubusercontent.com/your-repo/ChurnProject/main/quick-deploy.sh
chmod +x quick-deploy.sh
bash quick-deploy.sh yourdomain.com your@email.com
```

**4. Point Domain to EC2**
- Login to domain registrar (Namecheap, GoDaddy, etc)
- Add A Record: `@` → Your EC2 Public IP
- Wait 5-10 minutes for propagation

**5. Visit Your Domain**
```
https://yourdomain.com
```

✅ **DONE!** Your app is now live globally!

---

## **PATH 2: MANUAL (15 minutes) - Full Control 🛠️**

If quick-deploy doesn't work or you want full control:

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@YOUR_EC2_IP

# Clone repo
git clone https://github.com/your-username/ChurnProject.git
cd ChurnProject

# Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L \
  "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install SSL
sudo apt-get install -y certbot nginx

# Get Certificate
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email your@email.com \
  --agree-tos \
  --non-interactive

# Update nginx.conf with your domain
nano frontend/nginx.conf  # (edit server_name lines)

# Start services
docker compose up -d --build

# Configure Nginx
sudo cp frontend/nginx.conf /etc/nginx/sites-available/churnguard
sudo ln -sf /etc/nginx/sites-available/churnguard /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## **PATH 3: EASIEST (No Terminal) - AWS Elastic Beanstalk 💻**

If you don't want to use terminal:

1. **AWS Console** → Elastic Beanstalk → Create Environment
2. **Platform:** Docker
3. **Upload:** docker-compose.yml
4. **Environment Variables:**
   - `REACT_APP_API_URL=https://yourdomain.com`
5. **Done!** AWS handles everything including HTTPS

---

## **VERIFICATION CHECKLIST**

After deployment, verify everything works:

```bash
✅ Can access: https://yourdomain.com
✅ Can see Indigo logo on page load
✅ Can see cinematic animations
✅ Can see "Built by Prabhmeet Singh Ahuja"
✅ Can click "Train Model & Generate Analytics"
✅ Charts appear after training
✅ API health: curl https://yourdomain.com/api/health
✅ API docs: https://yourdomain.com/api/docs (if exposed)
```

---

## **DOMAIN SETUP (Required for All Paths)**

### How to Point Domain to Your Server

**Option A: Namecheap (Recommended for beginners)**
```
1. Login to Namecheap.com
2. Dashboard → Manage Domain
3. Advanced DNS Tab
4. Add A Record:
   - Host: @
   - Value: YOUR_EC2_PUBLIC_IP (e.g., 54.123.456.789)
   - TTL: 30 min
5. Save and wait 5-10 minutes
```

**Option B: GoDaddy**
```
1. MyProducts → Domains
2. DNS Management
3. Edit A Records:
   - @ → YOUR_EC2_PUBLIC_IP
   - www → YOUR_EC2_PUBLIC_IP
4. Save and wait
```

**Option C: AWS Route 53 (Advanced)**
```
1. Route 53 → Hosted Zones → Create Hosted Zone
2. Enter domain name
3. Create A Record:
   - Name: yourdomain.com
   - Type: A
   - Value: YOUR_EC2_PUBLIC_IP
4. Update domain registrar's nameservers to Route 53 ones
```

---

## **COST BREAKDOWN**

| Item | Cost | Duration | Notes |
|------|------|----------|-------|
| Domain | $8-15 | 1 year | Renewals typically same price |
| EC2 t2.micro | FREE | 12 months | Free tier - AWS free account |
| Storage (30GB) | FREE | Forever* | Part of free tier |
| SSL Certificate | FREE | Lifetime | Let's Encrypt auto-renew |
| Data Transfer | ~$0.09/GB | Per month | First 1GB free/month |
| **TOTAL Year 1** | **$8-15** | - | Essentially free! |
| **TOTAL Year 2+** | **$8-15** | - | Same (unless heavy traffic) |

\*AWS free tier is 12 months. After that, t2.micro costs ~$10/month if you keep it running.

---

## **MONITORING & MAINTENANCE**

### Check Status
```bash
# SSH into EC2
ssh -i key.pem ubuntu@YOUR_EC2_IP

# View logs
docker compose logs -f

# View specific service
docker compose logs -f backend
docker compose logs -f frontend

# Check health
curl https://yourdomain.com/api/health
```

### Auto SSL Renewal
```bash
# Already configured by quick-deploy.sh
# Certbot auto-renews every 60 days via cron

# Check renewal status
sudo certbot certificates
```

### Update Application
```bash
cd ChurnProject
git pull origin main
docker compose up -d --build
```

---

## **TROUBLESHOOTING**

### Domain not working?
```bash
# Check DNS propagation
nslookup yourdomain.com
# Should show your EC2 IP

# If not, wait 5-10 more minutes and try again
# Or use: https://www.whatsmydns.net
```

### Can't access via HTTPS?
```bash
# Check certificate
sudo certbot certificates

# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Check ports
sudo ss -tlnp | grep -E ':(80|443)'
```

### Can't SSH to EC2?
```bash
# Check key permissions
chmod 400 key.pem

# Check security group allows SSH (port 22)
# Check instance is running
# Verify public IP is correct
```

### Services not running?
```bash
# Check Docker
docker ps -a

# Restart services
docker compose restart

# View logs
docker compose logs
```

---

## **SHARE YOUR APP**

Once live on `https://yourdomain.com`, you can:

✅ Share the URL everywhere (works on any device, any internet)  
✅ No more "localhost" restrictions  
✅ Works on mobile, laptop, tablet, etc.  
✅ Survives internet outages by being stateless  
✅ Scalable to handle thousands of requests  

---

## **SECURITY BEST PRACTICES**

```bash
1. ✅ Use HTTPS only (configured by default)
2. ✅ Use strong SSH key (already done with EC2)
3. ✅ Enable auto-renewal for SSL (configured)
4. ✅ Keep instance updated: sudo apt-get update && sudo apt-get upgrade
5. ✅ Use security groups to restrict access
6. ✅ Monitor logs regularly
7. ✅ Backup data if storing anything important
```

---

## **NEXT LEVEL UPGRADES**

Once deployed, you can:

- 📊 Set up CloudWatch monitoring (AWS)
- 📧 Configure email alerts for errors
- 🌍 Add CDN (CloudFront) for faster global access
- 🔄 Set up auto-scaling for traffic spikes
- 🗃️ Add database (RDS) for persistent data
- 📈 Implement analytics and tracking

---

## **QUICK REFERENCE - COMMANDS**

```bash
# SSH to EC2
ssh -i key.pem ubuntu@YOUR_EC2_IP

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Check health
curl https://yourdomain.com/api/health

# SSL certificate status
sudo certbot certificates

# Update code
git pull && docker compose up -d --build

# System stats
docker stats
```

---

## **SUPPORT & RESOURCES**

- AWS Help: https://console.aws.amazon.com/support
- Docker Docs: https://docs.docker.com
- Let's Encrypt: https://community.letsencrypt.org
- Certbot: https://certbot.eff.org
- Stack Overflow: Tag with [aws], [docker], [ssl]

---

## **FINAL CHECKLIST**

Before launching:

- [ ] AWS Account created
- [ ] EC2 key pair created and saved
- [ ] Domain registered
- [ ] SSH access verified
- [ ] `quick-deploy.sh` or manual steps executed
- [ ] Domain pointing to EC2 IP
- [ ] DNS propagated (5-10 minutes)
- [ ] Can access https://yourdomain.com
- [ ] Logo and animations visible
- [ ] Can train model and see charts
- [ ] API health check working

---

## **FINALLY!**

Your ChurnGuard Pro is now:

🌍 **Live on the internet**  
🔒 **Secured with HTTPS**  
📱 **Accessible from anywhere**  
🚀 **Production-ready**  
💰 **Costs almost nothing**  

**Share it with:**
- Team members
- Stakeholders
- Clients
- Portfolio
- Anyone worldwide!

---

**Built with ❤️ by Prabhmeet Singh Ahuja**  
**ChurnGuard Pro - Indigo Airlines Intelligence Platform**

Visit: `https://yourdomain.com` (after deployment)
