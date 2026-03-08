# Complete ChurnGuard Pro Deployment (EC2 + Domain + SSL)

Complete end-to-end deployment guide for `indigoairlineschurnguardpro.com` on AWS with free SSL/HTTPS.

---

## Phase 1: Domain Registration (5 minutes)

### Option A: AWS Route 53 (Recommended - All in AWS)
1. AWS Console → Route 53 → Registered domains
2. Click **Register domain**
3. Search: `indigoairlineschurnguardpro.com`
4. Click **Add to cart** → **Continue** 
5. Fill contact info, check privacy settings
6. Complete purchase (~$12/year)
7. Wait for validation email and domain activation (10-30 min)

### Option B: Namecheap (~$8.88/year)
1. Go to https://www.namecheap.com
2. Search: `indigoairlineschurnguardpro.com`
3. Add to cart → Checkout → Complete purchase
4. Login to dashboard
5. **Keep open for DNS configuration later**

### Option C: GoDaddy
1. Go to https://www.godaddy.com
2. Search: `indigoairlineschurnguardpro.com`
3. Add to cart → Checkout → Complete purchase
4. Login to dashboard
5. **Keep open for DNS configuration later**

---

## Phase 2: Create EC2 Instance (5 minutes)

### Step 1: Launch Instance
1. Go to https://console.aws.amazon.com
2. Search and click **EC2**
3. Click **Instances** → **Launch instances**

### Step 2: Configure Instance
- **Name**: `churnguard-pro`
- **AMI**: Search "Ubuntu 22.04" → Select **Ubuntu 22.04 LTS (HVM)** (free tier)
- **Instance type**: `t2.micro` (free tier)
- **Architecture**: 64-bit (x86)

### Step 3: Create Key Pair
- Click **Create new key pair**
- **Name**: `churnguard-key`
- **Type**: RSA
- **Format**: `.pem` (Linux/Mac) or `.ppk` (Windows)
- Click **Create key pair** → **Download** (SAVE THIS FILE!)

### Step 4: Security Group
- Click **Create security group**
- **Name**: `churnguard-sg`
- **Description**: ChurnGuard security group

**Add inbound rules** (3 rules):
1. Type: SSH, Port: 22, Source: 0.0.0.0/0
2. Type: HTTP, Port: 80, Source: 0.0.0.0/0
3. Type: HTTPS, Port: 443, Source: 0.0.0.0/0

### Step 5: Storage
- Leave default (8 GB free tier eligible)

### Step 6: Launch
- Click **Launch instance**
- ✅ Instance launching...

### Step 7: Get Public IP
1. Go to **Instances**
2. Click your `churnguard-pro` instance
3. Copy **Public IPv4 address** (e.g., `54.123.45.67`)
4. **Note this down!**

---

## Phase 3: Configure DNS (5 minutes)

### If using AWS Route 53:
1. Route 53 → **Hosted zones**
2. Click your domain `indigoairlineschurnguardpro.com`
3. Click **Create record**
   - **Name**: Leave blank (for root domain)
   - **Type**: A
   - **Value**: Your EC2 public IP (e.g., 54.123.45.67)
   - Click **Create records**
4. Create another record for `www`:
   - **Name**: `www`
   - **Type**: A
   - **Value**: Your EC2 public IP
   - Click **Create records**

### If using Namecheap:
1. Namecheap dashboard → Your domains
2. Click **Manage** next to your domain
3. Go to **Advanced DNS**
4. Delete existing A records
5. Add new A records:
   - **Type**: A, **Host**: @, **Value**: Your EC2 public IP, **TTL**: Automatic
   - **Type**: A, **Host**: www, **Value**: Your EC2 public IP, **TTL**: Automatic
6. Save changes

### If using GoDaddy:
1. GoDaddy dashboard → Your products
2. Click **DNS** next to your domain
3. Find A records, update:
   - **Host**: @, **Points to**: Your EC2 public IP
   - **Host**: www, **Points to**: Your EC2 public IP
4. Save changes

---

## Phase 4: Deploy Application (10 minutes)

### Step 1: SSH to EC2 Instance
```bash
# Windows PowerShell (if .pem file saved)
ssh -i "C:\path\to\churnguard-key.pem" ubuntu@YOUR_PUBLIC_IP

# Linux/Mac
ssh -i ~/churnguard-key.pem ubuntu@YOUR_PUBLIC_IP

# Accept fingerprint: type "yes" and press Enter
```

### Step 2: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 3: Clone Repository
```bash
git clone https://github.com/sprabh12029-prsh/ChurnGuard-Pro.git
cd ChurnGuard-Pro
```

### Step 4: Run Deployment Script
```bash
bash quick-deploy.sh indigoairlineschurnguardpro.com your@email.com
```

**This script will automatically:**
- ✅ Install Docker & Docker Compose
- ✅ Build Docker images for frontend & backend
- ✅ Start containers
- ✅ Request Let's Encrypt SSL certificate (FREE)
- ✅ Configure Nginx reverse proxy
- ✅ Setup automatic SSL renewal

### Step 5: Wait for DNS Propagation
- DNS typically takes 5-10 minutes to propagate globally
- Check status: ```bash
nslookup indigoairlineschurnguardpro.com
```

---

## Phase 5: Launch Application (2 minutes)

### Once DNS resolves:
1. Open browser: **https://indigoairlineschurnguardpro.com**
2. You should see:
   - Indigo Airlines logo animation
   - ChurnGuard Pro dashboard
   - Full HTTPS with green lock icon

### Verify Everything:
- ✅ Visit `https://indigoairlineschurnguardpro.com` - Main app
- ✅ Visit `https://indigoairlineschurnguardpro.com/api/health` - API health check
- ✅ Certificate is valid (green lock icon)
- ✅ SSL renewal auto-configured

---

## Troubleshooting

### "Connection refused" or "Cannot reach server"
- Instance might still be starting (wait 2-3 min)
- Check security group has HTTP/HTTPS enabled
- Verify public IP is correct

### "Certificate error" or "Not secure"
- SSL may still be provisioning (wait 2-3 min)
- Check nginx logs: `sudo docker logs churnguard-frontend`

### "Domain not found"
- DNS not propagated yet (wait 5-10 min)
- Check DNS settings in registrar dashboard
- Verify A record points to correct EC2 IP

### "503 Service Unavailable"
- Backend container might be crashed
- Check logs: `sudo docker logs churnguard-backend`
- Restart: `sudo docker-compose restart backend`

---

## Cost Summary

| Item | Cost | Duration |
|------|------|----------|
| EC2 t2.micro | FREE | 12 months |
| Domain | ~$10-12 | 1 year |
| SSL Certificate | FREE | Auto-renews |
| **TOTAL** | **~$10-12** | **1 year** |

---

## Next Steps

Your ChurnGuard Pro application is now live on `https://indigoairlineschurnguardpro.com` and globally accessible!

- 📊 Share the URL with stakeholders
- 🔄 Access the dashboard for churn predictions
- 📈 Monitor ML model performance
- 🔐 All traffic encrypted with SSL/HTTPS

---

## Support

For issues, check logs:
```bash
# SSH to instance and run:
sudo docker-compose logs -f
```

Need to rebuild?
```bash
sudo docker-compose down
sudo docker-compose up --build -d
```
