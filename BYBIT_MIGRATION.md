# 🔄 Migración a Bybit Exchange

## ✅ Cambios Realizados

### 1. **Exchange actualizado en config.json**
```json
"exchange": {
    "name": "bybit",  // Cambiado de "binance"
    "pair_whitelist": [
        "BTC/USDT:USDT",  // Formato Bybit para Spot
        "ETH/USDT:USDT"
    ]
}
```

### 2. **Variables de entorno necesarias**

Debes actualizar estas variables en **Easypanel → trading-bot → github → Environment**:

```bash
EXCHANGE_API_KEY=QI74buZG3M5uXqIkoa
EXCHANGE_SECRET=xNs413FW1XtYaSmgZxMMrNCpGl8XH5kG7QLg
```

**IMPORTANTE**: Reemplaza las antiguas credenciales de Binance con estas de Bybit.

---

## 🔍 Diferencias Bybit vs Binance

| Aspecto | Binance | Bybit |
|---------|---------|-------|
| **Formato de pares** | `BTC/USDT` | `BTC/USDT:USDT` |
| **Restricciones geográficas** | ❌ Bloquea regiones | ✅ Menos restricciones |
| **API Rate Limits** | 1200/min | 120/min (más conservador) |
| **Comisiones Spot** | 0.1% | 0.1% |

---

## 📋 Pasos para completar el despliegue

### ✅ Paso 1: Actualizar variables en Easypanel

1. Ve a: **Easypanel → Proyecto `trading-bot` → App `github` → Environment**
2. Busca las variables:
   ```
   EXCHANGE_API_KEY
   EXCHANGE_SECRET
   ```
3. **Reemplaza** los valores con:
   ```
   EXCHANGE_API_KEY=QI74buZG3M5uXqIkoa
   EXCHANGE_SECRET=xNs413FW1XtYaSmgZxMMrNCpGl8XH5kG7QLg
   ```

### ✅ Paso 2: Redeploy automático

Después del commit, Easypanel detectará el cambio y reiniciará la app automáticamente con:
- ✅ Exchange: Bybit
- ✅ Pares: BTC/USDT, ETH/USDT
- ✅ Sin restricciones geográficas

### ✅ Paso 3: Verificar logs

Después del redeploy, verifica en los logs que veas:
```
✅ Using Exchange "Bybit"
✅ Instance is running with dry_run enabled
✅ BTC/USDT:USDT - analyzing...
```

---

## ⚠️ Notas importantes

1. **Formato de pares**: Bybit usa `BTC/USDT:USDT` para Spot trading (el `:USDT` indica que es mercado Spot)
2. **Rate limits**: Bybit tiene límites más conservadores, pero suficientes para nuestro bot
3. **API Keys**: Solo tienen permisos de Spot Trading + Read Wallet (sin retiros por seguridad)
4. **Testing**: El bot arrancará en `dry_run` (simulación) para validar primero

---

## 🚀 Próximos pasos después del despliegue

1. Monitorear logs primeras 24h
2. Verificar que detecte señales correctamente
3. Validar que la estrategia funcione igual que en Binance
4. Después de 1-2 semanas exitosas → considerar live trading

---

## 🆘 Troubleshooting

**Si ves error "Invalid symbol"**:
- Verifica que los pares tengan formato `:USDT` al final
- Bybit requiere este formato para distinguir Spot de Derivados

**Si ves error de API Key**:
- Confirma que las variables de entorno estén correctas en Easypanel
- Verifica que la API key tenga permisos de Spot Trading
