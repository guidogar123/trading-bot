#!/bin/bash
# Dual Exchange Trading Bot Deployment Script
# Deploys both Bybit and Binance bots on Hetzner server

set -e

echo "🚀 Deploying Dual Exchange Trading Bots..."

# Navigate to project directory
cd /root/trading-bot

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker stop freqtrade-bot 2>/dev/null || true
docker stop binance-bot 2>/dev/null || true
docker rm freqtrade-bot 2>/dev/null || true
docker rm binance-bot 2>/dev/null || true

# Rebuild image with latest code
echo "🏗️ Building Docker image..."
docker build -t trading-bot .

# Start Bybit bot (port 8080)
echo "▶️ Starting Bybit bot..."
docker run -d \
    --name freqtrade-bot \
    --restart unless-stopped \
    -p 8080:8080 \
    --env-file .env \
    -v $(pwd)/user_data:/app/user_data \
    trading-bot

# Start Binance bot (port 8081)
echo "▶️ Starting Binance bot..."
docker run -d \
    --name binance-bot \
    --restart unless-stopped \
    -p 8081:8081 \
    -e EXCHANGE_API_KEY=${BINANCE_API_KEY} \
    -e EXCHANGE_SECRET=${BINANCE_API_SECRET} \
    -e TELEGRAM_TOKEN=${TELEGRAM_TOKEN} \
    -e TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID} \
    -v $(pwd)/user_data:/app/user_data \
    trading-bot \
    freqtrade trade --config user_data/config_binance.json --strategy GridScalpingHybrid

# Wait for containers to start
echo "⏳ Waiting for bots to initialize..."
sleep 5

echo ""
echo "✅ ¡Dual Exchange Bots Deployed Successfully!"
echo ""
echo "📊 Bot Status:"
echo ""
echo "🔵 Bybit Bot:"
echo "   - Container: freqtrade-bot"
echo "   - API Port: 8080"
echo "   - Dashboard: http://95.216.202.233:8080"
echo "   - Pairs: BTC, ETH, SOL, BNB, XRP, ADA, AVAX, MATIC, DOT, LINK"
echo ""
echo "🟢 Binance Bot:"
echo "   - Container: binance-bot"
echo "   - API Port: 8081"
echo "   - Dashboard: http://95.216.202.233:8081"
echo "   - Pairs: LTC, ATOM, FIL, UNI, DOGE, TRX, AAVE, ALGO, XLM, VET"
echo ""
echo "🔐 Credentials:"
echo "   - Bybit Dashboard: http://95.216.202.233:8080"
echo "     Username: guido | Password: TradingBot2026!"
echo "   - Binance Dashboard: http://95.216.202.233:8081"
echo "     Username: guido | Password: BinanceBot2026!"
echo ""
echo "📋 Useful Commands:"
echo "   - View Bybit logs: docker logs -f freqtrade-bot"
echo "   - View Binance logs: docker logs -f binance-bot"
echo "   - Stop all bots: docker stop freqtrade-bot binance-bot"
echo "   - Restart all bots: docker restart freqtrade-bot binance-bot"
echo ""
