# 🚀 Quick Start Guide - Trading Bot

## ✅ Setup Completo

Tu bot está **100% configurado** y listo para usar!

### Estado Actual

| Componente | Estado |
|------------|--------|
| Freqtrade 2025.12 | ✅ Instalado |
| Python 3.14.2 | ✅ Configurado |
| Estrategia GridScalpingHybrid | ✅ Detectada |
| API Keys Binance | ✅ Configuradas |
| Entorno Virtual | ✅ Activo |

---

## 📊 Próximos Pasos

### 1️⃣ Activar Entorno Virtual

```powershell
cd C:\Users\guido\OneDrive\G2INNOVATION\TRADING_AUTOMATICO
.\venv\Scripts\Activate.ps1
```

### 2️⃣ Descargar Datos para Backtesting (10 min)

```powershell
freqtrade download-data `
  --exchange binance `
  --pairs BTC/USDT ETH/USDT SOL/USDT BNB/USDT `
  --timerange 20231001-20240101 `
  --timeframe 5m
```

### 3️⃣ Ejecutar Backtest (5 min)

```powershell
freqtrade backtesting `
  --strategy GridScalpingHybrid `
  --timerange 20231001-20240101 `
  --config user_data\config.json
```

### 4️⃣ Ver Resultados

```powershell
freqtrade backtesting-show
```

**Criterios de éxito**:
- ✅ Win rate > 50%
- ✅ Profit factor > 1.5
- ✅ Max drawdown < 15%
- ✅ Average daily profit > $10

### 5️⃣ Iniciar Paper Trading

Si los resultados del backtest son buenos:

```powershell
freqtrade trade `
  --config user_data\config.json `
  --strategy GridScalpingHybrid
```

> **Nota**: El bot está en modo `dry_run=true` (dinero virtual). No usará dinero real.

---

## 🎯 Estrategia Configurada

**GridScalpingHybrid**
- ✅ 3 señales de compra (RSI, MACD, Grid)
- ✅ 1 señal de venta
- ✅ Stop Loss: 2%
- ✅ Take Profit: 3%
- ✅ Timeframe: 5 minutos
- ✅ Pares: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT

---

## 🔍 Comandos Útiles

```powershell
# Ver versión
freqtrade --version

# Listar estrategias
freqtrade list-strategies --userdir user_data

# Ver ayuda
freqtrade --help

# Ver configuración
freqtrade show-config --config user_data\config.json

# Optimizar estrategia (después de backtest exitoso)
freqtrade hyperopt --strategy GridScalpingHybrid --epochs 100
```

---

## ⚠️ Importante

- 🔒 Tu API de Binance **NO tiene permisos de retiro** (seguro)
- 📊 El bot está en **modo paper trading** (dinero virtual)
- 🧪 Ejecuta **backtest antes de live trading**
- ⏱️ Paper trading por **mínimo 2 semanas**
- 💰 Empieza con **capital pequeño** cuando vayas a live

---

## 📁 Archivos Importantes

- `user_data/config.json` - Configuración del bot
- `user_data/strategies/GridScalpingHybrid.py` - Tu estrategia
- `.env` - API keys (NUNCA compartir)
- `README.md` - Documentación completa

---

**¡Bot listo para operar! Empieza con el paso 1.** 🎉
