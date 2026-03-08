#!/bin/bash

###############################################################################
# ChurnGuard Pro - AWS EC2 Deployment Script
# This script automates the deployment of the full stack on AWS EC2
# Author: Prabhmeet Singh Ahuja
# Usage: bash deploy-aws.sh
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   ChurnGuard Pro - AWS EC2 Deployment Script               ║${NC}"
echo -e "${BLUE}║   Built by Prabhmeet Singh Ahuja                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"

# Check if running on AWS EC2 instance
if ! curl -s http://169.254.169.254/latest/meta-data/instance-id &> /dev/null; then
    echo -e "${RED}✗ Not running on AWS EC2 instance${NC}"
    echo "This script should be run on an EC2 instance. Exiting..."
    exit 1
fi

echo -e "${GREEN}✓ Running on AWS EC2${NC}\n"

# Step 1: System Update
echo -e "${YELLOW}[1/8] Updating system packages...${NC}"
sudo apt-get update -y
sudo apt-get upgrade -y
echo -e "${GREEN}✓ System updated${NC}\n"

# Step 2: Install Docker
echo -e "${YELLOW}[2/8] Installing Docker...${NC}"
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh
echo -e "${GREEN}✓ Docker installed${NC}\n"

# Step 3: Install Docker Compose
echo -e "${YELLOW}[3/8] Installing Docker Compose...${NC}"
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
echo -e "${GREEN}✓ Docker Compose installed${NC}\n"

# Step 4: Install Git
echo -e "${YELLOW}[4/8] Installing Git...${NC}"
sudo apt-get install -y git
echo -e "${GREEN}✓ Git installed${NC}\n"

# Step 5: Clone Repository
echo -e "${YELLOW}[5/8] Cloning repository...${NC}"
if [ -d "churnproject" ]; then
    cd churnproject
    git pull origin main
else
    # Replace with your repository URL
    git clone https://github.com/yourusername/churnproject.git
    cd churnproject
fi
echo -e "${GREEN}✓ Repository cloned${NC}\n"

# Step 6: Create Environment File
echo -e "${YELLOW}[6/8] Creating environment configuration...${NC}"
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

cat > .env << EOF
API_HOST=0.0.0.0
API_PORT=8000
REACT_APP_API_URL=http://${PUBLIC_IP}:8000
ENVIRONMENT=production
EOF

echo -e "${GREEN}✓ Environment configured${NC}"
echo "  Public IP: ${PUBLIC_IP}"
echo "  API URL: http://${PUBLIC_IP}:8000"
echo ""

# Step 7: Build and Start Containers
echo -e "${YELLOW}[7/8] Building and starting Docker containers...${NC}"
docker-compose up -d --build
echo -e "${GREEN}✓ Containers started${NC}\n"

# Step 8: Health Check
echo -e "${YELLOW}[8/8] Performing health checks...${NC}"
sleep 10

BACKEND_HEALTH=$(curl -s http://localhost:8000/api/health | grep -o "healthy" || echo "down")
FRONTEND_STATUS=$(curl -s http://localhost | grep -o "html" || echo "down")

if [ "$BACKEND_HEALTH" == "healthy" ]; then
    echo -e "${GREEN}✓ Backend API: HEALTHY${NC}"
else
    echo -e "${RED}✗ Backend API: UNHEALTHY${NC}"
fi

if [ "$FRONTEND_STATUS" == "html" ]; then
    echo -e "${GREEN}✓ Frontend: OPERATIONAL${NC}"
else
    echo -e "${RED}✗ Frontend: DOWN${NC}"
fi

# Final Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Deployment Complete!                                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Access your application at:${NC}"
echo "  🌐 Frontend:   http://${PUBLIC_IP}"
echo "  📡 Backend API: http://${PUBLIC_IP}:8000"
echo "  📊 API Docs:   http://${PUBLIC_IP}:8000/docs"
echo "  ❤️  Health:     http://${PUBLIC_IP}:8000/api/health"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart services: docker-compose restart"
echo "  View containers:  docker-compose ps"
echo ""
echo -e "${GREEN}✓ ChurnGuard Pro is now live and accessible globally!${NC}\n"
