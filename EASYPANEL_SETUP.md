# 🚀 Setup Rápido - Easypanel

## ✅ Configuración Optimizada

Tu bot está configurado para **700MB RAM**:
- ✅ 2 pares de trading (BTC/USDT, ETH/USDT)
- ✅ Stake: $50 por trade
- ✅ Max 2 trades simultáneos
- ✅ Dry-run mode (sin dinero real)

---

## 📋 Paso 1: Subir a GitHub

### Dame tu usuario de GitHub

Ejecutaré estos comandos:
```powershell
git remote add origin https://github.com/TU-USUARIO/trading-bot.git
git push -u origin main
```

**O hazlo tú**:
1. Crear repo en GitHub: https://github.com/new
   - Name: `trading-bot`
   - Private: ✅
   - NO marcar README, .gitignore, etc

2. Ejecutar:
```powershell
cd C:\Users\guido\OneDrive\G2INNOVATION\TRADING_AUTOMATICO
git remote add origin https://github.com/TU-USUARIO/trading-bot.git
git push -u origin main
```

---

## 📋 Paso 2: Crear App en Easypanel

### 2.1 New App
1. Click **"+ Nuevo"** → **"App"**
2. Name: `trading-bot`

### 2.2 Source
- **Type**: GitHub
- **Repository**: `TU-USUARIO/trading-bot`
- **Branch**: `main`
- **Auto Deploy**: ✅ (recomendado)

### 2.3 Build
- **Build Method**: Dockerfile
- **Dockerfile Path**: `./Dockerfile`
- **Context**: `/`

### 2.4 Environment Variables

**Click "Add Variable"** y agregar estas (IMPORTANTE):

```env
EXCHANGE_API_KEY=xYRBUDX0k7Fu9xV2dFO7SJHIRnlpJ5jlUPS1O8dMOgDBf9xMt0osJAMkmbeym5lC
EXCHANGE_SECRET=Xl5zoTZbqQ0pGCwZZBeL0yQTaOkiZQj8Xt6J67Nh2Xc1xhA8VDzruxDBZdXl7S5N
```

### 2.5 Resources

**Memory Limit**: 512 MB
**CPU Limit**: 0.5 cores
**Restart Policy**: Always

### 2.6 Deploy

Click **"Deploy"** y espera 2-3 minutos.

---

## 📊 Paso 3: Verificar

### Ver Logs
1. Click en tu app `trading-bot`
2. Tab "Logs"
3. Deberías ver:
```
✓ Freqtrade successfully loaded
✓ Using strategy GridScalpingHybrid
✓ Dry run is enabled
✓ Running with 2 open trades
```

### Monitorear
- Los logs mostrarán señales de compra/venta
- Es simulación (dry_run), no dinero real
- Revisa cada 6-12 horas

---

## ⚙️ Variables de Entorno (Completas)

Si quieres más control, puedes agregar todas estas:

```env
# Exchange (OBLIGATORIAS)
EXCHANGE_API_KEY=xYRBUDX0k7Fu9xV2dFO7SJHIRnlpJ5jlUPS1O8dMOgDBf9xMt0osJAMkmbeym5lC
EXCHANGE_SECRET=Xl5zoTZbqQ0pGCwZZBeL0yQTaOkiZQj8Xt6J67Nh2Xc1xhA8VDzruxDBZdXl7S5N

# Trading Config (OPCIONALES - ya están en config.json)
DRY_RUN=true
INITIAL_CAPITAL=1000
MAX_OPEN_TRADES=2
STAKE_AMOUNT=50

# Telegram (OPCIONAL)
# TELEGRAM_TOKEN=bot123456:ABC...
# TELEGRAM_CHAT_ID=123456789
```

---

## 📈 Próximos 24-48 Horas

### Qué esperar:
- ✅ Bot arranca y lee mercado
- ✅ Calcula indicadores (RSI, MACD, etc)
- ✅ Genera señales de compra/venta
- ✅ Ejecuta trades simulados
- ✅ Logs muestran actividad

### Qué monitorear:
1. **RAM usage** en Easypanel → Metrics
   - Debe estar < 500MB
   - Si llega a 512MB → posible problema

2. **Logs** cada 6-12 horas
   - Ver trades ejecutados
   - Ver ganancias/pérdidas simuladas

3. **Errores**
   - API errors → revisar keys
   - OOM errors → necesita más RAM

---

## 🔄 Updates Futuros

Cuando hagas cambios:

```powershell
# Local
git add .
git commit -m "Descripción del cambio"
git push

# Easypanel desplegará automáticamente!
```

---

## 🆘 Troubleshooting

### Bot no arranca
```
Easypanel → Logs
Ver error específico
```

### Error de API keys
```
Verificar variables de entorno
EXCHANGE_API_KEY y EXCHANGE_SECRET
```

### Consume mucha RAM
```
Reducir a 1 par solo:
Editar config.json → solo BTC/USDT
```

---

## ✅ Checklist

- [ ] Código subido a GitHub
- [ ] App creada en Easypanel
- [ ] GitHub conectado
- [ ] Variables de entorno configuradas
- [ ] Memory limit: 512MB
- [ ] Bot desplegado
- [ ] Logs verificados
- [ ] Monitoreo activo

---

## 🎉 Ready!

Una vez completado:
- Bot corre 24/7 en la nube
- Sin costo adicional (usas tu Easypanel)
- Trades simulados para validar estrategia
- Logs para análisis diario

**Después de 1-2 semanas**:
Si funciona bien → considerar live trading o migrar a Hetzner para más pares.
