# 🚀 Deployment en AWS VPS

## ✅ Ventajas de Usar AWS

- 🌐 **Sin restricciones DNS**: Acceso directo a APIs de exchanges
- ⏰ **24/7 uptime**: El bot nunca se apaga
- ⚡ **Baja latencia**: Servidores cerca de exchanges
- 💰 **Económico**: Desde $3.50/mes con Lightsail
- 🔒 **Seguro**: Aislado de tu red local
- 📊 **Monitoreo**: CloudWatch integrado

---

## 📋 Opciones de Deployment

### Opción 1: AWS Lightsail (Recomendado - Más Fácil) 💡

**Costo**: $3.50 - $5/mes
**Specs**: 512MB RAM, 1 vCPU, 20GB SSD

**Ventajas**:
- Precio fijo mensual
- Configuración simple
- IP estática incluida
- Panel web fácil de usar

### Opción 2: AWS EC2 (Más Flexible)

**Costo**: ~$4-8/mes (t3.micro o t4g.micro)
**Specs**: 1GB RAM, 1-2 vCPU

**Ventajas**:
- Más opciones de configuración
- Auto-scaling (si creces)
- Integración con otros servicios AWS

---

## 🎯 Guía de Deployment AWS Lightsail (Recomendado)

### Paso 1: Crear Instancia Lightsail

1. **Ir a AWS Lightsail**
   - https://lightsail.aws.amazon.com/

2. **Crear instancia**
   - Click "Create instance"
   - Región: **US East (N. Virginia)** o **Asia Pacific (Singapore)**
   - Plataforma: **Linux/Unix**
   - Blueprint: **Ubuntu 22.04 LTS**

3. **Seleccionar plan**
   - **$5/mes**: 1GB RAM, 1 vCPU, 40GB SSD ← Recomendado
   - o $3.50/mes si quieres ahorrar (mínimo)

4. **Nombre**: `trading-bot`

5. **Click "Create instance"**

---

### Paso 2: Configurar SSH

**Opción A: Desde navegador** (Más fácil)
- En Lightsail, click en la instancia
- Click "Connect using SSH" (browser)

**Opción B: SSH local**
```powershell
# Descargar key desde Lightsail
# Luego conectar:
ssh -i trading-bot-key.pem ubuntu@<IP_PUBLICA>
```

---

### Paso 3: Setup Automatizado

Una vez conectado al servidor, ejecuta:

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python 3.11+
sudo apt install python3 python3-pip python3-venv git curl -y

# 3. Clonar tu repositorio (si usas Git)
# O subir archivos vía SFTP

# 4. Instalar Freqtrade
cd ~
mkdir trading_bot
cd trading_bot

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar Freqtrade
pip install freqtrade[all]

# Inicializar estructura
freqtrade create-userdir --userdir user_data

# 5. Configurar como servicio systemd (para que corra 24/7)
# Ver sección siguiente
```

---

### Paso 4: Transferir Archivos

**Opción A: Git** (Recomendado)
```bash
# Si tienes tu código en GitHub
git clone <tu-repo-url>
cd <tu-repo>
```

**Opción B: SFTP**
```powershell
# Desde tu PC local
# Usar WinSCP o FileZilla
# Servidor: <IP_PUBLICA>
# Usuario: ubuntu
# Key: trading-bot-key.pem

# Subir carpetas:
# - user_data/strategies/GridScalpingHybrid.py
# - user_data/config.json
# - .env (con API keys)
```

**Opción C: Copiar directo** (más rápido para testing)
```bash
# En el servidor, crear archivos manualmente
nano user_data/strategies/GridScalpingHybrid.py
# Pegar el código de tu estrategia

nano user_data/config.json
# Pegar tu configuración

nano .env
# Pegar tus API keys
```

---

### Paso 5: Configurar como Servicio (24/7)

Crear archivo de servicio systemd:

```bash
sudo nano /etc/systemd/system/trading-bot.service
```

Pegar esta configuración:

```ini
[Unit]
Description=Freqtrade Trading Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/trading_bot
Environment="PATH=/home/ubuntu/trading_bot/venv/bin"
ExecStart=/home/ubuntu/trading_bot/venv/bin/freqtrade trade --config user_data/config.json --strategy GridScalpingHybrid
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar y iniciar el servicio:

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Iniciar bot
sudo systemctl start trading-bot

# Habilitar auto-inicio  
sudo systemctl enable trading-bot

# Ver status
sudo systemctl status trading-bot

# Ver logs en tiempo real
sudo journalctl -u trading-bot -f
```

---

## 🐳 Opción Alternativa: Docker (Avanzado)

Si prefieres usar Docker (más portable):

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Crear Dockerfile
nano Dockerfile
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install freqtrade[all]

COPY user_data /app/user_data
COPY .env /app/.env

CMD ["freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "GridScalpingHybrid"]
```

**Ejecutar:**
```bash
# Build
docker build -t trading-bot .

# Run noche y día
docker run -d --name trading-bot --restart unless-stopped trading-bot

# Ver logs
docker logs -f trading-bot
```

---

## 📊 Monitoreo

### Ver Logs
```bash
# Logs del servicio
sudo journalctl -u trading-bot -f

# Logs de Freqtrade
tail -f user_data/logs/freqtrade.log
```

### Comandos Útiles
```bash
# Detener bot
sudo systemctl stop trading-bot

# Reiniciar bot
sudo systemctl restart trading-bot

# Ver estado
sudo systemctl status trading-bot

# Ver trades (si usas dry-run)
freqtrade show-trades --config user_data/config.json
```

---

## 🔒 Seguridad

### 1. Firewall
```bash
# Permitir solo SSH
sudo ufw allow 22
sudo ufw enable
```

### 2. Permisos del .env
```bash
chmod 600 .env
```

### 3. Actualizar API Keys
Edita `.env` en el servidor:
```bash
nano .env
# Pegar tus API keys de Binance
```

---

## 💰 Costos Estimados

| Servicio | Costo Mensual |
|----------|---------------|
| Lightsail $5/mes | $5.00 |
| Transfer datos | ~$0.50 |
| **Total** | **~$5.50/mes** |

**Return on Investment**:
- Si tu bot genera $10/día = $300/mes
- Costo VPS = $5.50/mes  
- **Ganancia neta**: $294.50/mes 🎉

---

## 🚀 Script de Setup Automatizado

He creado un script que hace todo automático. 

**En el servidor AWS**:
```bash
# Descargar y ejecutar
curl -o setup_aws.sh https://raw.githubusercontent.com/tu-repo/setup_aws.sh
bash setup_aws.sh
```

---

## ✅ Checklist de Deployment

- [ ] Crear instancia Lightsail ($5/mes)
- [ ] Conectar por SSH
- [ ] Instalar Python + Freqtrade
- [ ] Transferir archivos (estrategia, config, .env)
- [ ] Configurar servicio systemd
- [ ] Iniciar bot
- [ ] Verificar logs
- [ ] Configurar monitoreo

---

## 🆘 Troubleshooting

**Bot no inicia**:
```bash
sudo systemctl status trading-bot
sudo journalctl -u trading-bot -n 50
```

**Error de API keys**:
```bash
nano .env
# Verificar que las keys están correctas
sudo systemctl restart trading-bot
```

**Sin internet**:
```bash
ping api.binance.com
# Debería funcionar desde AWS
```

---

## 📞 Próximos Pasos

1. **Crear instancia Lightsail** (5 minutos)
2. **Ejecutar script de setup** (10 minutos)
3. **Transferir archivos** (5 minutos)
4. **Iniciar bot** (1 minuto)
5. **Monitorear** (continuo)

**¿Quieres que te ayude paso a paso con el deployment?**
