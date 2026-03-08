# 🎉 Deploy on FREE Public Domain (& Free AWS)

## ZERO COST DEPLOYMENT

**Total cost: $0.00** for first 12 months!

---

## **STEP 1: Get FREE Domain (Freenom)**

### Register Free Domain
1. Go to: https://www.freenom.com
2. Click **"Find a new FREE domain"**
3. Search for your desired name:
   - `yourname.tk` (Tokelau)
   - `yourname.ml` (Mali) 
   - `yourname.ga` (Gabon)
   - `yourname.cf` (Central African Republic)
   - All are **completely FREE**!

4. Choose 12-month period (free)
5. Click **"Checkout"**
6. Create free account (or login)
7. Complete checkout
8. **You now have a FREE domain!**

### Example:
- If you want: `churnguard.tk` or `myproject.ml`
- It's 100% FREE for 12 months!

---

## **STEP 2: Create AWS Free Tier EC2** 

(Same as before - completely FREE for 12 months)

### Go to AWS Console
1. https://console.aws.amazon.com/ec2/
2. Click **"Launch Instances"**

### Configure:
```
Instance name: ChurnGuard-Pro
AMI: Ubuntu Server 22.04 LTS
Instance type: t2.micro (FREE)
Key pair: Create new → churnguard-key.pem (save it!)

Firewall (Security Group):
  - SSH: Port 22, Source: My IP
  - HTTP: Port 80, Source: 0.0.0.0/0
  - HTTPS: Port 443, Source: 0.0.0.0/0

Storage: 30GB (FREE)

Cost: $0.00 (free tier)
```

3. Click **"Launch Instance"**
4. Wait for green "running" status
5. **Copy Public IPv4 address** (e.g., 54.123.456.789)

---

## **STEP 3: Point FREE Domain to AWS**

### In Freenom Dashboard:
1. Go to: https://my.freenom.com/
2. Login
3. Click **"My Domains"**
4. Select your domain (e.g., churnguard.tk)
5. Click **"Manage Domain"**
6. Click **"Management Tools"** → **"Nameservers"**
7. Select **"Custom Nameservers"**
8. Add Amazon nameservers (from AWS Route 53):
   
   **First, get Route 53 nameservers:**
   - AWS Console → Route 53
   - Hosted Zones → Create Hosted Zone
   - Enter domain: churnguard.tk
   - Copy the 4 nameservers (NS records)
   - Format: ns-123.awsdns-45.com
   
9. Paste all 4 nameservers in Freenom
10. Click **"Save Changes"**

---

## **STEP 4: Setup AWS Route 53 (DNS)**

### In AWS Console:
1. Go to Route 53
2. **Hosted Zones** → **Create Hosted Zone**
3. Domain name: `churnguard.tk` (your free domain)
4. Click **"Create Hosted Zone"**
5. You'll see 4 nameservers - **these go in Freenom** (step 3 above)
6. Click into your zone
7. Click **"Create Record"**
   - Record name: `churnguard.tk`
   - Type: **A**
   - Value: YOUR_EC2_PUBLIC_IP (from step 2)
   - TTL: 300
   - Click **"Create Records"**

8. Create another record:
   - Record name: `www.churnguard.tk`
   - Type: **A**
   - Value: YOUR_EC2_PUBLIC_IP (same)
   - TTL: 300
   - Click **"Create Records"**

---

## **STEP 5: SSH to EC2 & Deploy**

### Connect to your server:

**Windows (PowerShell):**
```powershell
cd C:\path\to\churnguard-key.pem
icacls churnguard-key.pem /grant:r "$($env:USERNAME):(F)"
ssh -i churnguard-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

**Mac/Linux:**
```bash
cd ~/Downloads
chmod 400 churnguard-key.pem
ssh -i churnguard-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### On EC2 instance:
```bash
# Clone repo
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/ChurnProject.git
cd ChurnProject

# Run deployment with YOUR FREE DOMAIN
chmod +x quick-deploy.sh
bash quick-deploy.sh churnguard.tk your@email.com
```

**This will:**
- ✅ Install Docker
- ✅ Install Docker Compose
- ✅ Get FREE SSL certificate (Let's Encrypt)
- ✅ Configure Nginx
- ✅ Start all services
- ✅ Setup auto SSL renewal

**Takes ~5-10 minutes**

---

## **STEP 6: Wait for DNS Propagation**

DNS changes take **5-10 minutes** (sometimes up to 24 hours).

Check if ready:
```bash
# On your local machine (NOT EC2):
nslookup churnguard.tk

# Should show: YOUR_EC2_PUBLIC_IP
```

Or use: https://www.whatsmydns.net

---

## **STEP 7: Test Your App**

Once DNS is ready:

1. Open browser
2. Go to: `https://churnguard.tk` (your domain)
3. Should see:
   - ✅ Indigo logo with glow
   - ✅ "ChurnGuard Pro" title
   - ✅ Animations
   - ✅ "Built by Prabhmeet Singh Ahuja"
   - ✅ Full dashboard

---

## **COST BREAKDOWN**

| Item | Cost | Duration | Notes |
|------|------|----------|-------|
| Domain (Freenom) | **FREE** | 12 months | Auto-renew for free |
| EC2 t2.micro | **FREE** | 12 months | AWS free tier |
| Storage 30GB | **FREE** | Forever* | Free tier included |
| SSL Certificate | **FREE** | Lifetime | Let's Encrypt auto-renew |
| Data Transfer | **FREE** | 1 GB/month | Free tier allowance |
| **TOTAL COST** | **$0.00** | 12 months | Completely FREE! |

\*AWS free tier is 12 months. After that, costs ~$10/month if you keep it running.

---

## **QUICK REFERENCE**

```bash
# SSH to instance
ssh -i key.pem ubuntu@YOUR_EC2_IP

# Check if deployed correctly
curl https://churnguard.tk/api/health

# View logs
docker compose logs -f

# Check DNS
nslookup churnguard.tk

# Check SSL cert
sudo certbot certificates
```

---

## **TROUBLESHOOTING**

### DNS not resolving?
```bash
# Check if nameservers are set in Freenom (Step 3)
# May take 24 hours to fully propagate
nslookup churnguard.tk
# Should return: YOUR_EC2_IP
```

### HTTPS shows error?
```bash
# Check certificate
sudo certbot certificates

# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Check ports
sudo ss -tlnp | grep -E ':(80|443)'
```

### Can't connect via SSH?
```
- Check AWS security group allows SSH (port 22)
- Verify you're using correct key.pem file
- Check instance is running in AWS console
- Correct IP address used
```

### Domain shows registrar parking page?
```
- DNS hasn't propagated yet (wait 5-10 min)
- Nameservers not correctly set in Freenom
- Check: https://www.whatsmydns.net/
```

---

## **MONITOR YOUR APP**

```bash
# SSH to instance regularly
ssh -i key.pem ubuntu@YOUR_EC2_IP

# Check container status
docker ps

# View recent logs
docker compose logs --tail=50

# Check server health
curl https://churnguard.tk/api/health

# Monitor storage
df -h

# Check memory
free -h
```

---

## **RENEW YOUR FREE DOMAIN**

After 12 months, Freenom domains auto-renew for FREE!

Just make sure Freenom account doesn't expire.

---

## **NEXT STEPS - SUPER SIMPLE!**

1. ✅ Go to Freenom.com → Register FREE domain (.tk, .ml, etc)
2. ✅ Go to AWS Console → Create EC2 instance (t2.micro, free)
3. ✅ Get EC2 public IP
4. ✅ In Freenom: Set nameservers to AWS Route 53
5. ✅ In AWS Route 53: Create A records pointing to EC2 IP
6. ✅ SSH to EC2 and run `quick-deploy.sh`
7. ✅ Wait for DNS (5-10 min)
8. ✅ Visit `https://yourdomain.tk` 🎉

---

## **FINAL RESULT**

Your ChurnGuard Pro will be:

✅ **Live on the internet** at `https://churnguard.tk`  
✅ **Completely HTTPS secured** (green lock 🔒)  
✅ **FREE domain** + **FREE server** = **$0 cost**  
✅ **Accessible worldwide** from any device  
✅ **Production-ready** enterprise app  
✅ **Auto SSL renewal** (no manual work)  
✅ **Works perfectly** for 12+ months  

---

## **EXAMPLE WORKFLOW**

```
Day 1:
- Register free domain: churnguard.tk (Freenom) ✅
- Create EC2 instance (AWS) ✅
- SSH and run quick-deploy.sh ✅

Day 1-2:
- Wait for DNS propagation ⏳

Day 2:
- Visit: https://churnguard.tk ✅
- App is live! 🎉
- Show anyone: "https://churnguard.tk" 🌍
```

---

**That's it!** You now have a **free, professional, globally-accessible web application!**

Built by: Prabhmeet Singh Ahuja  
Platform: ChurnGuard Pro - Indigo Airlines Intelligence System

---

## **Need Help?**

- Freenom issues: https://www.freenom.com/en/faq.html
- AWS issues: https://console.aws.amazon.com/support
- SSL issues: https://community.letsencrypt.org
- Docker issues: https://docs.docker.com
- DNS issues: https://www.whatsmydns.net
