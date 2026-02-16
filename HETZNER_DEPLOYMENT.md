# 🚀 Despliegue en Hetzner Cloud

Guía completa para deployar el bot de trading en Hetzner Cloud.

---

## 📋 Pre-requisitos

- ✅ Servidor Hetzner CX23 comprado
- ✅ Código en GitHub: `https://github.com/guidogar123/trading-bot.git`
- ✅ API Keys de Bybit configuradas
- ✅ Terminal con SSH (PowerShell en Windows)

---

## 🔑 Paso 1: Obtener credenciales del servidor

Hetzner te envió un **email** con:
- **IP del servidor** (ejemplo: `195.201.123.45`)
- **Usuario**: `root`
- **Contraseña temporal**

**IMPORTANTE**: Guarda estas credenciales de forma segura.

---

## 🖥️ Paso 2: Conectar al servidor vía SSH

### Windows PowerShell:

```powershell
ssh root@TU_IP_AQUI
```

**Ejemplo**:
```powershell
ssh root@195.201.123.45
```

**Primera conexión**:
1. Te preguntará: `Are you sure you want to continue connecting (yes/no)?`
   - Escribe: `yes` y presiona Enter
2. Ingresa la **contraseña temporal** que recibiste por email
3. Te pedirá cambiar la contraseña:
   - Ingresa la contraseña actual
   - Crea una nueva contraseña segura
   - Confírmala

**Resultado esperado**:
```
root@hostname:~#
```

---

## 📦 Paso 3: Actualizar sistema e instalar Docker

Copia y pega estos comandos **uno por uno**:

### 3.1 Actualizar paquetes del sistema:
```bash
apt update && apt upgrade -y
```

### 3.2 Instalar Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```

### 3.3 Instalar Docker Compose:
```bash
apt install docker-compose -y
```

### 3.4 Verificar instalación:
```bash
docker --version
docker-compose --version
```

**Resultado esperado**:
```
Docker version 27.x.x
docker-compose version 1.29.x
```

---

## 📥 Paso 4: Clonar repositorio de GitHub

```bash
cd /root
git clone https://github.com/guidogar123/trading-bot.git
cd trading-bot
```

**Verificar que se clonó correctamente**:
```bash
ls -la
```

Deberías ver:
- `Dockerfile`
- `user_data/`
- `bot_config/`
- etc.

---

## ⚙️ Paso 5: Configurar variables de entorno

### 5.1 Crear archivo .env:
```bash
nano .env
```

### 5.2 Copiar y pegar esta configuración:

```bash
# Bybit API Keys
EXCHANGE_API_KEY=QI74buZG3M5uXqIkoa
EXCHANGE_SECRET=xNs413FW1XtYaSmgZxMMrNCpGl8XH5kG7QLg

# Telegram (opcional)
TELEGRAM_TOKEN=8404087496:AAHhLD-2-Wc2NJwMxJX_T2hJgC8uSzy1Qjw
TELEGRAM_CHAT_ID=TU_CHAT_ID_AQUI
```

**Si ya tienes tu Chat ID de Telegram**, reemplaza `TU_CHAT_ID_AQUI` con el número.

### 5.3 Guardar y salir:
- Presiona `Ctrl + O` (guardar)
- Presiona `Enter` (confirmar)
- Presiona `Ctrl + X` (salir)

---

## 🐳 Paso 6: Construir y ejecutar el bot

### 6.1 Construir imagen Docker:
```bash
docker build -t trading-bot .
```

**Duración**: 3-5 minutos

### 6.2 Ejecutar el bot:
```bash
docker run -d \
  --name freqtrade-bot \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/user_data:/app/user_data \
  trading-bot
```

**Parámetros**:
- `-d` = Ejecutar en segundo plano
- `--restart unless-stopped` = Reiniciar automáticamente si se cae
- `--env-file .env` = Cargar variables de entorno
- `-v` = Montar directorio de datos (persistencia)

---

## ✅ Paso 7: Verificar que esté corriendo

### 7.1 Ver logs en tiempo real:
```bash
docker logs -f freqtrade-bot
```

**Busca estas líneas** (confirman éxito):
```
✅ Using Exchange "Bybit"
✅ Instance is running with dry_run enabled
✅ Using max_open_trades: 2
✅ BTC/USDT:USDT - analyzing...
✅ ETH/USDT:USDT - analyzing...
```

**Para salir de los logs**: Presiona `Ctrl + C`

### 7.2 Ver estado del contenedor:
```bash
docker ps
```

Deberías ver:
```
CONTAINER ID   IMAGE          STATUS         NAMES
abc123...      trading-bot    Up 2 minutes   freqtrade-bot
```

---

## 🔧 Comandos útiles

### Ver logs del bot:
```bash
docker logs -f freqtrade-bot
```

### Detener el bot:
```bash
docker stop freqtrade-bot
```

### Iniciar el bot:
```bash
docker start freqtrade-bot
```

### Reiniciar el bot:
```bash
docker restart freqtrade-bot
```

### Ver estado:
```bash
docker ps -a
```

### Eliminar contenedor (si necesitas recrearlo):
```bash
docker stop freqtrade-bot
docker rm freqtrade-bot
```

---

## 📊 Monitoreo

### Opción 1: Logs de Docker
```bash
docker logs -f freqtrade-bot
```

### Opción 2: FreqUI (Interfaz Web) - Opcional

Si quieres activar la interfaz web:

1. Edita `user_data/config.json`:
```bash
nano user_data/config.json
```

2. Cambia:
```json
"api_server": {
    "enabled": true,
    "listen_ip_address": "0.0.0.0",
    "listen_port": 8080
}
```

3. Reinicia el bot:
```bash
docker restart freqtrade-bot
```

4. Accede desde tu navegador:
```
http://TU_IP_SERVIDOR:8080
```

---

## 🔒 Seguridad (Opcional pero recomendado)

### 1. Configurar firewall:
```bash
ufw allow 22/tcp
ufw allow 8080/tcp
ufw enable
```

### 2. Crear usuario no-root:
```bash
adduser trading
usermod -aG sudo trading
usermod -aG docker trading
```

---

## 🆘 Troubleshooting

### Bot no arranca:
```bash
docker logs freqtrade-bot
```

### Error de API Keys:
Verifica que `.env` tenga las credenciales correctas:
```bash
cat .env
```

### Error de geo-restricción:
Verifica la ubicación del servidor:
```bash
curl ipinfo.io
```

Debería mostrar **Alemania** (Hetzner).

---

## 🎯 Siguiente paso

Una vez que el bot esté corriendo exitosamente:
1. ✅ Monitorea logs las primeras 24 horas
2. ✅ Configura notificaciones de Telegram
3. ✅ Revisa performance semanal
4. ✅ Considera activar live trading después de 2-4 semanas de validación

**¡Listo! Tu bot está 24/7 en la nube sin restricciones geográficas! 🚀**
