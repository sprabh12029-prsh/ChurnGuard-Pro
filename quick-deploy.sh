#!/bin/bash

################################################################################
# ChurnGuard Pro - QUICK PUBLIC DEPLOYMENT
# One command to deploy on AWS with your domain
# Usage: bash quick-deploy.sh yourdomain.com
################################################################################

set -e

DOMAIN=${1:-"yourdomain.com"}
EMAIL=${2:-"your@email.com"}

if [ -z "$1" ]; then
    echo "❌ Domain required!"
    echo "Usage: bash quick-deploy.sh yourdomain.com your@email.com"
    exit 1
fi

echo "╔════════════════════════════════════════════════════╗"
echo "║   ChurnGuard Pro - Public Domain Deployment        ║"
echo "║   Domain: $DOMAIN"
echo "║   Email:  $EMAIL"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Step 1: System Setup
echo "📦 [1/6] Installing dependencies..."
sudo apt-get update -y > /dev/null 2>&1
sudo apt-get install -y curl git docker.io docker-compose certbot nginx > /dev/null 2>&1
sudo usermod -aG docker $USER
echo "✅ Dependencies installed"
echo ""

# Step 2: Clone Repository
echo "📥 [2/6] Cloning ChurnGuard Pro..."
if [ ! -d "ChurnProject" ]; then
    git clone https://github.com/prabhmeet/ChurnProject.git
fi
cd ChurnProject
echo "✅ Repository ready"
echo ""

# Step 3: Get SSL Certificate
echo "🔒 [3/6] Requesting SSL certificate from Let's Encrypt..."
sudo certbot certonly --standalone \
    -d $DOMAIN \
    -d www.$DOMAIN \
    --email $EMAIL \
    --agree-tos \
    --non-interactive \
    --keep-until-expiring 2>&1 | grep -v "^$"
echo "✅ SSL certificate ready"
echo ""

# Step 4: Configure Nginx
echo "⚙️  [4/6] Configuring Nginx..."
sudo tee /etc/nginx/sites-available/churnguard > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/churnguard /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t > /dev/null 2>&1
sudo systemctl restart nginx
echo "✅ Nginx configured"
echo ""

# Step 5: Deploy Docker
echo "🐳 [5/6] Deploying Docker containers..."
docker compose up -d --build 2>&1 | grep -E "(Creating|Created|Starting|Started)" || true
sleep 5
echo "✅ Docker services started"
echo ""

# Step 6: Verify
echo "✔️  [6/6] Verifying deployment..."
sleep 3
HEALTH=$(curl -s http://localhost:8000/api/health | grep -q "healthy" && echo "✅ HEALTHY" || echo "❌ DOWN")
FRONTEND=$(curl -s http://localhost:3000 | grep -q "ChurnGuard" && echo "✅ RUNNING" || echo "❌ DOWN")

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║        🎉 DEPLOYMENT COMPLETE!                     ║"
echo "╠════════════════════════════════════════════════════╣"
echo "║ 🌐 Frontend:  https://$DOMAIN"
echo "║ 📊 API:       https://$DOMAIN/api/health"
echo "║ 📚 API Docs:  https://$DOMAIN/api/docs"
echo "║                                                    ║"
echo "║ Backend Status:   $HEALTH"
echo "║ Frontend Status:  $FRONTEND"
echo "║                                                    ║"
echo "║ 📝 Author: Prabhmeet Singh Ahuja                  ║"
echo "║ 🚀 Ready for worldwide access!                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Setup auto-renewal
echo "⏰ Setting up automatic SSL renewal..."
sudo tee /usr/local/bin/renew-ssl-churnguard.sh > /dev/null <<'RENEW'
#!/bin/bash
certbot renew --quiet 2>/dev/null
sudo systemctl reload nginx 2>/dev/null
RENEW
sudo chmod +x /usr/local/bin/renew-ssl-churnguard.sh
(sudo crontab -l 2>/dev/null | grep -v "renew-ssl-churnguard"; echo "0 0 1 * * /usr/local/bin/renew-ssl-churnguard.sh") | sudo crontab -
echo "✅ Auto-renewal configured (checks monthly)"
echo ""

echo "═══════════════════════════════════════════════════"
echo "NEXT STEPS:"
echo "1. Point your domain DNS to this server's IP"
echo "2. Wait 5-10 minutes for DNS propagation"
echo "3. Visit https://$DOMAIN in your browser"
echo "4. Enjoy ChurnGuard Pro!"
echo "═══════════════════════════════════════════════════"
