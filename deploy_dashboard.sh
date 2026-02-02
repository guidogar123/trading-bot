#!/bin/bash
# FreqUI Dashboard Deployment Script for Hetzner Server
# This script sets up FreqUI with nginx reverse proxy

set -e

echo "🚀 Installing FreqUI Dashboard on Hetzner Server..."

# Update system
echo "📦 Updating system packages..."
apt-get update

# Install nginx if not already installed
echo "🔧 Installing nginx..."
apt-get install -y nginx

# Stop nginx temporarily
systemctl stop nginx

# Clone FreqUI if not exists
if [ ! -d "/root/frequi" ]; then
    echo "📥 Cloning FreqUI repository..."
    cd /root
    git clone https://github.com/freqtrade/frequi.git
fi

# Build FreqUI Docker image
echo "🏗️ Building FreqUI Docker image..."
cd /root/frequi
docker build -t frequi .

# Stop and remove old FreqUI container if exists
docker stop frequi 2>/dev/null || true
docker rm frequi 2>/dev/null || true

# Run FreqUI container on port 3000
echo "▶️ Starting FreqUI container..."
docker run -d \
    --name frequi \
    --restart unless-stopped \
    -p 127.0.0.1:3000:80 \
    frequi

# Configure nginx reverse proxy
echo "⚙️ Configuring nginx..."
cat > /etc/nginx/sites-available/freqtrade << 'EOF'
server {
    listen 80;
    server_name _;

    # Serve FreqUI
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Proxy API requests to Freqtrade bot
    location /api/ {
        proxy_pass http://127.0.0.1:8080/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PUT' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
        
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/freqtrade /etc/nginx/sites-enabled/freqtrade

# Remove default nginx site
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
nginx -t

# Start nginx
echo "✅ Starting nginx..."
systemctl start nginx
systemctl enable nginx

# Open firewall port 80
echo "🔓 Opening firewall port 80..."
ufw allow 80/tcp

echo ""
echo "✅ ¡FreqUI Dashboard instalado exitosamente!"
echo ""
echo "🌐 Accede a tu dashboard en:"
echo "   http://95.216.202.233"
echo ""
echo "🔐 Credenciales de login:"
echo "   API URL: http://95.216.202.233/api"
echo "   Username: guido"
echo "   Password: TradingBot2026!"
echo ""
echo "📊 El dashboard ahora está corriendo en tu servidor!"
