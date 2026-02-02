# Trading Bot - $10 USD Daily Target

Bot de trading automatizado usando Freqtrade con estrategia híbrida Grid + Scalping.

## 🎯 Objetivo

Generar **$10 USD de ganancia diaria** mediante trading automatizado de criptomonedas.

## 📊 Estrategia

- **Grid Trading (70%)**: Para mercados laterales
- **Scalping (30%)**: Para mercados volátiles
- **Capital recomendado**: $1,000 - $2,000 USD
- **Retorno esperado**: 0.5% - 1% diario

## 🔧 Stack Tecnológico

- **Framework**: Freqtrade
- **Exchange**: Binance
- **Pares**: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT
- **Timeframe**: 5 minutos
- **Indicadores**: RSI, MACD, Bollinger Bands, EMA, ATR

## 📁 Estructura del Proyecto

```
TRADING_AUTOMATICO/
├── freqtrade/              # Framework clonado de GitHub
├── bot_config/             # Configuraciones personalizadas
│   ├── GridScalpingHybrid.py    # Estrategia de trading
│   ├── config.json              # Configuración del bot
│   ├── risk_manager.py          # Módulo de gestión de riesgo
│   └── .env.example             # Template de variables de entorno
├── README.md               # Este archivo
└── docker-compose.yml      # Para deployment (próximamente)
```

## 🚀 Instalación

### 1. Requisitos Previos

```powershell
# Python 3.9 o superior
python --version

# Git
git --version
```

### 2. Clonar e Instalar Freqtrade

```powershell
# Ya clonado en este proyecto
cd freqtrade

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -e .
```

### 3. Configurar el Bot

```powershell
# Copiar configuración personalizada
copy ..\bot_config\GridScalpingHybrid.py user_data\strategies\
copy ..\bot_config\config.json user_data\

# Copiar template de variables de entorno
copy ..\bot_config\.env.example .env

# Editar .env con tus API keys
notepad .env
```

### 4. Configurar API Keys de Binance

1. Crear cuenta en [Binance](https://www.binance.com)
2. Ir a **API Management**
3. Crear nueva API Key
4. **Importante**: NO habilitar retiros
5. Copiar API Key y Secret al archivo `.env`

## 📖 Uso

### Paper Trading (Recomendado para empezar)

```powershell
# Activar entorno virtual
.venv\Scripts\activate

# Ejecutar en modo dry-run (dinero virtual)
freqtrade trade --config user_data\config.json --strategy GridScalpingHybrid --dry-run
```

### Backtesting (Probar estrategia con datos históricos)

```powershell
# Descargar datos históricos
freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timerange 20231001-20240101

# Ejecutar backtest
freqtrade backtesting --strategy GridScalpingHybrid --timerange 20231001-20240101

# Ver resultados
freqtrade backtesting-show
```

### Trading en Vivo (Después de validar)

```powershell
# IMPORTANTE: Solo después de resultados exitosos en paper trading

# 1. Editar config.json y cambiar:
#    "dry_run": false

# 2. Asegurar que API keys están configuradas

# 3. Iniciar bot
freqtrade trade --config user_data\config.json --strategy GridScalpingHybrid
```

## ⚙️ Configuración

### Risk Management

Configurado en `risk_manager.py`:

- **Stop Loss**: 2% por trade
- **Take Profit**: 3% por trade
- **Max Open Trades**: 5 simultáneos
- **Position Size**: 10% del capital por trade
- **Max Daily Drawdown**: 10%
- **Daily Target**: $10 USD

### Pares de Trading

Editables en `config.json`:

```json
"pair_whitelist": [
  "BTC/USDT",
  "ETH/USDT",
  "SOL/USDT",
  "BNB/USDT"
]
```

## 📊 Monitoreo

### Logs

```powershell
# Ver logs en tiempo real
tail -f user_data\logs\freqtrade.log
```

### Telegram Notifications (Opcional)

1. Crear bot de Telegram con [@BotFather](https://t.me/botfather)
2. Obtener Token
3. Obtener tu Chat ID con [@userinfobot](https://t.me/userinfobot)
4. Configurar en `.env`:

```bash
TELEGRAM_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

5. Habilitar en `config.json`:

```json
"telegram": {
  "enabled": true
}
```

## 🔒 Seguridad

- ✅ **NUNCA** habilitar permisos de retiro en API keys
- ✅ Usar autenticación de 2 factores en exchange
- ✅ NO commitear archivo `.env` a Git
- ✅ Empezar siempre con paper trading
- ✅ Monitorear el bot especialmente al inicio

## 📈 Optimización de Estrategia

```powershell
# Optimizar parámetros automáticamente
freqtrade hyperopt --strategy GridScalpingHybrid --epochs 100 --spaces buy sell roi stoploss

# Ver mejores resultados
freqtrade hyperopt-show
```

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

```powershell
# Asegurar que el entorno virtual está activado
.venv\Scripts\activate

# Reinstalar dependencias
pip install -e .
```

### Error: Exchange Authentication Failed

- Verificar API Key y Secret en `.env`
- Verificar que las IPs están en whitelist (si aplica)
- Verificar permisos de la API key

### Bot no hace trades

- Verificar que `dry_run: true` está en `config.json`
- Revisar logs para ver señales de compra/venta
- Verificar que los pares tienen suficiente liquidez

## 📚 Recursos

- [Documentación Freqtrade](https://www.freqtrade.io/)
- [Estrategias de ejemplo](https://github.com/freqtrade/freqtrade-strategies)
- [Comunidad Freqtrade](https://discord.gg/p7nuUNVfP7)

## ⚠️ Disclaimer

**El trading de criptomonedas conlleva riesgos significativos.** Este bot es una herramienta educativa y no garantiza ganancias. Nunca inviertas más de lo que puedes permitirte perder.

- Este software se proporciona "tal cual" sin garantías
- Los resultados pasados no garantizan resultados futuros
- Siempre haz tu propia investigación (DYOR)
- Empieza con capital pequeño y paper trading

## 📝 Roadmap

- [x] Estrategia Grid + Scalping
- [x] Risk management
- [x] Configuración para Binance
- [ ] Docker deployment
- [ ] Dashboard web (FreqUI)
- [ ] Notificaciones Telegram
- [ ] Backtesting completo
- [ ] Optimización con Hyperopt
- [ ] Multiple timeframe analysis

## 📄 Licencia

MIT License - Uso bajo tu propio riesgo.
