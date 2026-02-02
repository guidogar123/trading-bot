# 📱 Configuración de Telegram

## Paso 1: Obtener tu Chat ID

1. Abre Telegram y busca el bot: **@userinfobot**
2. Inicia conversación con `/start`
3. El bot te responderá con tu información, **copia el número de "Id"**
   
   Ejemplo:
   ```
   Id: 123456789  ← Este es tu CHAT_ID
   ```

## Paso 2: Actualizar variables de entorno en Easypanel

Ve a **Easypanel → Proyecto `trading-bot` → App `github` → Environment**

Agrega estas dos variables:

```
TELEGRAM_TOKEN=8404087496:AAHhLD-2-Wc2NJwMxJX_T2hJgC8uSzy1Qjw
TELEGRAM_CHAT_ID=TU_CHAT_ID_AQUI  ← Reemplaza con el ID del paso 1
```

## Paso 3: Reiniciar la app

Después de agregar las variables, haz click en **"Redeploy"** o **"Restart"**

## ✅ Verificación

Una vez reiniciado, el bot te enviará un mensaje de Telegram:
```
🤖 Trading Bot iniciado
Modo: DRY RUN
Pares: BTC/USDT, ETH/USDT
```

## 📊 Notificaciones que recibirás

- 💰 **Compras**: Cuando el bot simula una compra
- 💸 **Ventas**: Cuando el bot simula una venta
- ⚠️ **Alertas**: Errores o problemas
- 📈 **Resumen diario**: Performance del día
