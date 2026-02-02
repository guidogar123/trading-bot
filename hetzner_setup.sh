#!/bin/bash
# Script de setup automatizado para servidor Hetzner
# Instala Docker, clona el repo, configura el bot y lo ejecuta

set -e  # Detener en caso de error

echo "=========================================="
echo "  Configurando servidor Hetzner..."
echo "=========================================="
echo ""

# 1. Actualizar sistema
echo "[1/7] Actualizando sistema..."
apt update -qq && apt upgrade -y -qq

# 2. Instalar Docker
echo "[2/7] Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# 3. Instalar Docker Compose
echo "[3/7] Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt install -y docker-compose
fi

# Verificar instalación
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"

# 4. Clonar repositorio
echo "[4/7] Descargando codigo del bot..."
cd /root
if [ -d "trading-bot" ]; then
    echo "Directorio existente encontrado, actualizando..."
    cd trading-bot
    git pull
else
    git clone https://github.com/guidogar123/trading-bot.git
    cd trading-bot
fi

# 5. Configurar variables de entorno
echo "[5/7] Configurando credenciales..."
if [ ! -f .env ]; then
    echo "Creando archivo .env..."
    cat > .env << 'EOF'
# Bybit API Keys
EXCHANGE_API_KEY=QI74buZG3M5uXqIkoa
EXCHANGE_SECRET=xNs413FW1XtYaSmgZxMMrNCpGl8XH5kG7QLg

# Telegram (opcional - agrega tu Chat ID)
TELEGRAM_TOKEN=8404087496:AAHhLD-2-Wc2NJwMxJX_T2hJgC8uSzy1Qjw
TELEGRAM_CHAT_ID=
EOF
    echo "Archivo .env creado. Puedes editarlo con: nano .env"
else
    echo "Archivo .env ya existe, manteniendolo sin cambios"
fi

# 6. Construir imagen Docker
echo "[6/7] Construyendo imagen Docker (esto puede tardar 3-5 min)..."
docker build -t trading-bot .

# Detener contenedor anterior si existe
if docker ps -a | grep -q freqtrade-bot; then
    echo "Deteniendo contenedor anterior..."
    docker stop freqtrade-bot 2>/dev/null || true
    docker rm freqtrade-bot 2>/dev/null || true
fi

# 7. Ejecutar bot
echo "[7/7] Iniciando bot de trading..."
docker run -d \
  --name freqtrade-bot \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/user_data:/app/user_data \
  trading-bot

# Esperar 5 segundos para que el bot inicie
sleep 5

echo ""
echo "=========================================="
echo "  Verificando estado del bot..."
echo "=========================================="
docker ps | grep freqtrade-bot

echo ""
echo "=========================================="
echo "  Mostrando logs iniciales..."
echo "=========================================="
docker logs freqtrade-bot | tail -n 30

echo ""
echo "=========================================="
echo "  ✅ DEPLOYMENT COMPLETADO EXITOSAMENTE"
echo "=========================================="
echo ""
echo "El bot esta corriendo en modo DRY RUN (simulacion)"
echo ""
echo "Comandos utiles:"
echo "  - Ver logs en tiempo real:  docker logs -f freqtrade-bot"
echo "  - Ver estado:               docker ps"
echo "  - Reiniciar bot:            docker restart freqtrade-bot"
echo "  - Detener bot:              docker stop freqtrade-bot"
echo "  - Iniciar bot:              docker start freqtrade-bot"
echo ""
echo "Para editar configuracion:"
echo "  - Variables de entorno:     nano .env"
echo "  - Config del bot:           nano user_data/config.json"
echo ""
echo "Despues de editar, reinicia el bot con: docker restart freqtrade-bot"
echo ""
