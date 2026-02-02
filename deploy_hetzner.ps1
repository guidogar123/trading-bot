# Script de deployment automatizado para Hetzner
# Este script configura el servidor y despliega el bot automáticamente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Bot de Trading - Deployment Hetzner  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuración
$SERVER_IP = "95.216.202.233"
$SERVER_USER = "root"
$TEMP_PASSWORD = "Ar3UmrmmirM9AhewJ7st"

# API Keys desde global
$EXCHANGE_API_KEY = "QI74buZG3M5uXqIkoa"
$EXCHANGE_SECRET = "xNs413FW1XtYaSmgZxMMrNCpGl8XH5kG7QLg"
$TELEGRAM_TOKEN = "8404087496:AAHhLD-2-Wc2NJwMxJX_T2hJgC8uSzy1Qjw"

Write-Host "Configuracion:" -ForegroundColor Yellow
Write-Host "  - Servidor: $SERVER_IP" -ForegroundColor White
Write-Host "  - Exchange: Bybit" -ForegroundColor White
Write-Host "  - Modo: Dry Run (simulacion)" -ForegroundColor White
Write-Host ""

# Preguntar por nueva contraseña
Write-Host "IMPORTANTE: Necesitaras crear una nueva contrasena para el servidor" -ForegroundColor Yellow
$NEW_PASSWORD = Read-Host "Ingresa tu nueva contrasena para el servidor" -AsSecureString
$NEW_PASSWORD_PLAIN = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($NEW_PASSWORD))

# Telegram Chat ID (opcional)
Write-Host ""
$CHAT_ID = Read-Host "Ingresa tu Telegram Chat ID (opcional, presiona Enter para omitir)"
if ([string]::IsNullOrWhiteSpace($CHAT_ID)) {
    $CHAT_ID = ""
    Write-Host "  -> Notificaciones de Telegram deshabilitadas" -ForegroundColor Gray
} else {
    Write-Host "  -> Telegram configurado correctamente" -ForegroundColor Green
}

Write-Host ""
Write-Host "Iniciando deployment automatizado..." -ForegroundColor Cyan
Write-Host ""

# Crear script de setup remoto
$SETUP_SCRIPT = @"
#!/bin/bash
set -e

echo "=========================================="
echo "  Configurando servidor Hetzner..."
echo "=========================================="
echo ""

# 1. Actualizar sistema
echo "[1/7] Actualizando sistema..."
apt update -qq && apt upgrade -y -qq

# 2. Instalar Docker
echo "[2/7] Instalando Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh > /dev/null 2>&1
apt install -y docker-compose -qq

# 3. Verificar Docker
echo "[3/7] Verificando instalacion de Docker..."
docker --version
docker-compose --version

# 4. Clonar repositorio
echo "[4/7] Descargando codigo del bot..."
cd /root
if [ -d "trading-bot" ]; then
    rm -rf trading-bot
fi
git clone https://github.com/guidogar123/trading-bot.git
cd trading-bot

# 5. Configurar variables de entorno
echo "[5/7] Configurando credenciales..."
cat > .env << 'ENVEOF'
# Bybit API Keys
EXCHANGE_API_KEY=$EXCHANGE_API_KEY
EXCHANGE_SECRET=$EXCHANGE_SECRET

# Telegram
TELEGRAM_TOKEN=$TELEGRAM_TOKEN
TELEGRAM_CHAT_ID=$CHAT_ID
ENVEOF

# 6. Construir imagen Docker
echo "[6/7] Construyendo imagen Docker (esto puede tardar 3-5 min)..."
docker build -t trading-bot . > /dev/null 2>&1

# 7. Ejecutar bot
echo "[7/7] Iniciando bot de trading..."
docker run -d \
  --name freqtrade-bot \
  --restart unless-stopped \
  --env-file .env \
  -v \$(pwd)/user_data:/app/user_data \
  trading-bot

# Esperar 5 segundos
sleep 5

# Verificar estado
echo ""
echo "=========================================="
echo "  Verificando estado del bot..."
echo "=========================================="
docker ps | grep freqtrade-bot

echo ""
echo "Mostrando logs iniciales..."
echo "=========================================="
docker logs freqtrade-bot | tail -n 20

echo ""
echo "=========================================="
echo "  DEPLOYMENT COMPLETADO EXITOSAMENTE"
echo "=========================================="
echo ""
echo "Comandos utiles:"
echo "  - Ver logs:      docker logs -f freqtrade-bot"
echo "  - Reiniciar bot: docker restart freqtrade-bot"
echo "  - Detener bot:   docker stop freqtrade-bot"
echo ""
"@

# Guardar script temporalmente
$SETUP_SCRIPT_PATH = "$env:TEMP\hetzner_setup.sh"
$SETUP_SCRIPT | Out-File -FilePath $SETUP_SCRIPT_PATH -Encoding UTF8 -NoNewline

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Conectando al servidor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host "1. Cuando te pida 'Are you sure...', escribe: yes" -ForegroundColor White
Write-Host "2. Cuando te pida 'password:', pega: $TEMP_PASSWORD" -ForegroundColor White
Write-Host "3. Te pedira CAMBIAR la contrasena:" -ForegroundColor White
Write-Host "   - Current password: $TEMP_PASSWORD" -ForegroundColor White
Write-Host "   - New password: [la que ingresaste arriba]" -ForegroundColor White
Write-Host "   - Retype password: [la misma otra vez]" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Enter para continuar..." -ForegroundColor Green
Read-Host

# Ejecutar SSH y deployment
Write-Host "Conectando via SSH y ejecutando deployment..." -ForegroundColor Cyan
Write-Host ""

# Comando SSH interactivo
ssh ${SERVER_USER}@${SERVER_IP}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Script finalizado" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Yellow
Write-Host "1. Una vez conectado al servidor, ejecuta:" -ForegroundColor White
Write-Host "   bash < (curl -s https://raw.githubusercontent.com/guidogar123/trading-bot/main/hetzner_setup.sh)" -ForegroundColor Cyan
Write-Host ""
Write-Host "O copia el archivo hetzner_setup.sh al servidor y ejecutalo" -ForegroundColor Gray
