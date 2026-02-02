# ✅ Configuración Final - Easypanel

## 🎉 Código en GitHub
**URL**: https://github.com/guidogar123/trading-bot
**Branch**: main
**Commits**: 2

---

## 📋 Pasos en Easypanel (5 minutos)

### 1. Crear Nueva App
1. En Easypanel → **"+ Nuevo"** → **"App"**
2. **Name**: `trading-bot`
3. Click **"Create"**

---

### 2. Configurar Source

**GitHub Connection**:
- Click **"Source"** tab
- Type: **GitHub**
- Click **"Connect GitHub"**
- Autoriza con tu cuenta
- **Repository**: `guidogar123/trading-bot`
- **Branch**: `main`
- **Auto Deploy**: ✅ Activar

---

### 3. Configurar Build

**Docker Settings**:
- **Build Method**: `Dockerfile`
- **Dockerfile Path**: `./Dockerfile`
- **Build Context**: `/` (raíz)

---

### 4. Variables de Entorno (CRÍTICO)

Click **"Environment"** → **"Add Variable"**

Agregar **EXACTAMENTE** estas dos:

```
EXCHANGE_API_KEY
xYRBUDX0k7Fu9xV2dFO7SJHIRnlpJ5jlUPS1O8dMOgDBf9xMt0osJAMkmbeym5lC

EXCHANGE_SECRET
Xl5zoTZbqQ0pGCwZZBeL0yQTaOkiZQj8Xt6J67Nh2Xc1xhA8VDzruxDBZdXl7S5N
```

**Formato**:
- Variable 1: Name=`EXCHANGE_API_KEY` Value=`xYRBUDX0k7Fu9xV2dFO7SJHIRnlpJ5jlUPS1O8dMOgDBf9xMt0osJAMkmbeym5lC`
- Variable 2: Name=`EXCHANGE_SECRET` Value=`Xl5zoTZbqQ0pGCwZZBeL0yQTaOkiZQj8Xt6J67Nh2Xc1xhA8VDzruxDBZdXl7S5N`

---

### 5. Configurar Resources

**Limits** (para 700MB RAM disponibles):
- **Memory**: `512 MB` (suficiente para 2 pares)
- **CPU**: `0.5 cores`

**Restart Policy**:
- **Always** (para que se reinicie si falla)

---

### 6. Deploy

1. Click **"Deploy"**
2. **Espera 2-3 minutos** mientras:
   - Descarga código de GitHub
   - Construye Docker image
   - Instala Freqtrade
   - Arranca el bot

---

## 📊 Verificación

### Ver Logs (inmediatamente después de deploy)

1. Tab **"Logs"**
2. Deberías ver:

```
✓ Freqtrade successfully loaded
✓ Using strategy GridScalpingHybrid
✓ Dry run is enabled
✓ Running with 2 max open trades
✓ Validating pairs: ['BTC/USDT', 'ETH/USDT']
✓ Strategy started
```

### Si ves errores:

**Error: API keys invalid**
- Revisar variables de entorno
- Copiar/pegar sin espacios extras

**Error: Out of memory**
- Reducir memory limit a 512MB exacto
- O reducir a 1 solo par (BTC/USDT)

**Error: Cannot connect to binance**
- Normal desde Easypanel
- El bot intentará reconectar cada 30s

---

## 📈 Primer día (24 horas)

### Qué esperar:
- ✅ Bot lee precios cada 5 minutos
- ✅ Calcula indicadores (RSI, MACD, etc)
- ✅ Genera señales de compra/venta
- ✅ Ejecuta trades **simulados** (dry_run)
- ✅ Logs muestran actividad

### Monitorear:

**Cada 6 horas** (mínimo):
1. Tab **"Metrics"** → Ver RAM usage (debe ser < 450MB)
2. Tab **"Logs"** → Ver trades simulados
3. Buscar líneas como:
   ```
   Buy signal: BTC/USDT at $35,234
   Profit: +$2.45 (+0.7%)
   ```

**Cada 24 horas**:
1. Revisar total de trades
2. Ver win rate (trades ganadores vs perdedores)
3. Calcular profit simulado

---

## 🔄 Updates Futuros

Cuando quieras cambiar la estrategia:

```powershell
# En tu PC
cd C:\Users\guido\OneDrive\G2INNOVATION\TRADING_AUTOMATICO

# Editar archivos
# Por ejemplo: user_data/strategies/GridScalpingHybrid.py

# Commit y push
git add .
git commit -m "Optimizar señales de compra"
git push

# Easypanel desplegará automáticamente en 1-2 minutos!
```

---

## ⚙️ Ajustes Opcionales

### Telegram Notifications (opcional)

Si quieres recibir notificaciones:

1. Crear bot en Telegram con @BotFather
2. Obtener token y chat_id
3. Agregar variables de entorno:
   ```
   TELEGRAM_TOKEN=bot123456:ABC...
   TELEGRAM_CHAT_ID=123456789
   ```

### Aumentar pares (si funciona bien)

Si después de 1 semana quieres más pares:

1. Editar `user_data/config.json`
2. Agregar SOL/USDT o BNB/USDT
3. Aumentar max_open_trades a 3
4. Commit y push

---

## 🆘 Troubleshooting

### Bot se reinicia constantemente
```
Tab "Logs" → ver error específico
Probablemente OOM (out of memory)
Solución: reducir a 1 par solo
```

### No genera señales de compra
```
Normal los primeros 30-60 minutos
La estrategia espera condiciones específicas
Si después de 2 horas sin señales → revisar mercado
```

### Consume mucha RAM (>500MB)
```
Opciones:
A) Reducir a 1 par
B) Migrar a Hetzner (4GB RAM por $4.50/mes)
```

---

## ✅ Checklist Final

- [ ] App creada en Easypanel
- [ ] GitHub conectado (guidogar123/trading-bot)
- [ ] Variables de entorno configuradas
- [ ] Memory: 512MB
- [ ] Auto-deploy activado
- [ ] Deploy ejecutado
- [ ] Logs verificados
- [ ] Bot corriendo 24/7

---

## 🎉 ¡Listo!

Tu bot está:
- ✅ Corriendo 24/7 en la nube
- ✅ Trading automático (simulado)
- ✅ Sin costo adicional (usa tu Easypanel)
- ✅ Auto-deploy desde GitHub
- ✅ Optimizado para 700MB RAM

**Próximos pasos**:
1. Monitorear primeras 24-48 horas
2. Ver performance en dry_run
3. Después de 1-2 semanas → decidir si live trading
4. O migrar a servidor dedicado para más pares

**¡Felicidades! 🚀**
