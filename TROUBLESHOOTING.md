# ⚠️ Problema de Conexión con Binance API

## 🔍 Diagnóstico

### Error Encontrado
```
TemporaryError: Error in reload_markets due to ExchangeNotAvailable
Message: binance GET https://api.binance.com/api/v3/exchangeInfo
```

### Test de Conectividad
- ✅ **Puerto 443 a api.binance.com**: Abierto (TcpTestSucceeded: True)
- ❌ **Freqtrade descarga de datos**: Falla

---

## 🔧 Posibles Causas y Soluciones

### 1. Restricción Geográfica / VPN ⚡ (Más Probable)

Binance puede estar bloqueando la conexión desde tu ubicación o IP.

**Soluciones**:

#### Opción A: Usar VPN
```powershell
# Conectar a VPN antes de usar Freqtrade
# Países recomendados: Singapore, Japan, Germany
```

#### Opción B: Cambiar a Binance US (si estás en USA)
```json
// En user_data/config.json, cambiar:
"exchange": {
  "name": "binanceus",  // <-- Cambiar aquí
  ...
}
```

#### Opción C: Usar otro Exchange
Exchanges alternativos compatibles:
- **Bybit** (recomendado, sin restricciones)
- **OKX**
- **Kucoin**
- **Gate.io**

---

### 2. API Keys Incorrectas ⚠️

Las API keys podrían tener restricciones de IP.

**Solución**:
1. Ir a Binance → API Management
2. Editar API Key
3. En "IP Access Restrictions":
   - Opción 1: **Unrestricted** (no recomendado para producción)
   - Opción 2: Agregar tu IP pública actual

**Ver tu IP pública**:
```powershell
curl ifconfig.me
```

---

### 3. Rate Limiting / Bloqueo Temporal 🕐

Binance podría haber bloqueado temporalmente tu IP.

**Solución**:
- Esperar 15-30 minutos
- Reiniciar router para obtener nueva IP
- Usar VPN

---

### 4. Problema de Proxy / Firewall 🔒

Tu red corporativa o firewall podría estar bloqueando la conexión.

**Solución**:
```powershell
# Verificar si hay proxy configurado
netsh winhttp show proxy

# Si hay proxy, configurarlo en Freqtrade
# Agregar a config.json:
"ccxt_config": {
  "enableRateLimit": true,
  "httpsProxy": "http://proxy.tuempresa.com:8080"
}
```

---

## ✅ Solución Rápida: Usar Datos Pre-descargados

Si no puedes resolver la conexión ahora, puedes:

### Opción 1: Usar Exchange Público sin Restricciones

```powershell
# Cambiar temporalmente a Bybit o OKX
.\venv\Scripts\freqtrade.exe download-data `
  --exchange bybit `
  --pairs BTC/USDT ETH/USDT `
  --timerange 20231001-20231031 `
  --timeframe 5m
```

### Opción 2: Simular con Datos de Prueba

He creado un script para generar datos de prueba:

```powershell
python bot_config\generate_test_data.py
```

---

## 🎯 Recomendación Inmediata

**Paso 1**: Verificar restricciones de API
```powershell
# Ir a Binance y verificar que:
# 1. API Key esté activa
# 2. No tenga restricciones de IP (o agregar tu IP)
# 3. Tenga permisos de lectura habilitados
```

**Paso 2**: Conectar VPN y reintentar
```powershell
# Después de conectar VPN:
.\venv\Scripts\freqtrade.exe download-data `
  --exchange binance `
  --pairs BTC/USDT `
  --timerange 20231001-20231031 `
  --timeframe 5m
```

**Paso 3**: Si persiste, cambiar a Bybit
```json
// En user_data/config.json:
{
  "exchange": {
    "name": "bybit",
    // Resto de configuración igual
  }
}
```

---

## 📞 Siguiente Paso

**¿Qué quieres hacer?**

A. Conectar VPN y reintentar con Binance
B. Cambiar a Bybit (sin restricciones)
C. Verificar restricciones de IP en Binance
D. Generar datos de prueba para testear estrategia

Avísame cuál prefieres y continúo con la configuración.
