#!/bin/bash

# =============================================================================
# Trading Bot - AWS Setup Script
# Automated deployment for AWS Lightsail/EC2
# =============================================================================

set -e  # Exit on error

echo "============================================="
echo "  Trading Bot - AWS Setup"
echo "  Automated Installation"
echo "============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Please do not run as root${NC}"
  exit 1
fi

# Step 1: Update system
echo -e "${YELLOW}[1/7] Updating system...${NC}"
sudo apt update
sudo apt upgrade -y

# Step 2: Install dependencies
echo -e "${YELLOW}[2/7] Installing dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl wget htop

# Step 3: Create project directory
echo -e "${YELLOW}[3/7] Creating project directory...${NC}"
mkdir -p ~/trading_bot
cd ~/trading_bot

# Step 4: Create virtual environment
echo -e "${YELLOW}[4/7] Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Step 5: Install Freqtrade
echo -e "${YELLOW}[5/7] Installing Freqtrade (this may take a few minutes)...${NC}"
pip install --upgrade pip
pip install freqtrade[all]

# Step 6: Initialize Freqtrade
echo -e "${YELLOW}[6/7] Initializing Freqtrade structure...${NC}"
freqtrade create-userdir --userdir user_data

# Step 7: Create systemd service
echo -e "${YELLOW}[7/7] Creating systemd service...${NC}"

sudo tee /etc/systemd/system/trading-bot.service > /dev/null <<EOF
[Unit]
Description=Freqtrade Trading Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/trading_bot
Environment="PATH=$HOME/trading_bot/venv/bin"
ExecStart=$HOME/trading_bot/venv/bin/freqtrade trade --config user_data/config.json --strategy GridScalpingHybrid
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

echo ""
echo "============================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Upload your files:"
echo "   - user_data/strategies/GridScalpingHybrid.py"
echo "   - user_data/config.json"
echo "   - .env (with API keys)"
echo ""
echo "2. Start the bot:"
echo "   sudo systemctl start trading-bot"
echo ""
echo "3. Enable auto-start:"
echo "   sudo systemctl enable trading-bot"
echo ""
echo "4. View logs:"
echo "   sudo journalctl -u trading-bot -f"
echo ""
echo "5. Check status:"
echo "   sudo systemctl status trading-bot"
echo ""
echo "============================================="
echo ""
echo "Project directory: ~/trading_bot"
echo "Activate venv: source ~/trading_bot/venv/bin/activate"
echo ""
