# Cómo Obtener API Keys de Binance

## 📋 Guía Paso a Paso

### 1. Crear Cuenta en Binance
- Ve a [binance.com](https://www.binance.com/es/register)
- Registra con email y contraseña segura
- Verifica tu email

### 2. Completar KYC (Verificación de Identidad)
- Menú → Perfil → Identificación
- Sube documento de identidad
- Toma selfie de verificación
- Espera aprobación (usualmente 10-30 minutos)

### 3. Crear API Key

1. **Acceder a API Management:**
   - Perfil → API Management
   - O directo: https://www.binance.com/es/my/settings/api-management

2. **Crear Nueva API Key:**
   - Click "Create API"
   - Nombre: `FreqTrade Bot` o similar
   - Confirma con 2FA (email/SMS)

3. **Configurar Permisos:**
   - ✅ **Enable Spot & Margin Trading** (activar)
   - ❌ **Enable Withdrawals** (NO activar - seguridad)
   - ❌ **Enable Futures** (NO activar - no lo necesitas)
   - ❌ **Enable Internal Transfer** (NO activar)

4. **Restricción de IP (Opcional pero Recomendado):**
   - Click "Restrict access to trusted IPs"
   - Agregar IP: `95.216.202.233` (tu servidor Hetzner)
   - Esto previene acceso no autorizado

5. **Guardar Credenciales:**
   - **API Key**: Copia y guarda (visible siempre)
   - **Secret Key**: ⚠️ COPIA AHORA - solo se muestra una vez!

---

## 🔐 Información a Guardar

Después de crear la API key, tendrás:

```
API Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API Secret: yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

⚠️ **IMPORTANTE:**
- Guarda el Secret Key inmediatamente
- No compartas estas credenciales
- Si pierdes el Secret, deberás crear nueva API key

---

## 🚀 Después de Obtener las Keys

### Opción 1: Deployment Manual

SSH al servidor y actualiza `.env`:

```bash
ssh root@95.216.202.233
cd /root/trading-bot

# Agregar credenciales de Binance al .env
nano .env

# Agregar estas líneas al final:
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_secret_key_aqui

# Guardar (Ctrl+O, Enter, Ctrl+X)
```

Luego deployar:
```bash
git pull origin main
chmod +x deploy_dual_bots.sh
./deploy_dual_bots.sh
```

### Opción 2: Pídeme Ayuda

Simplemente comparte las keys conmigo (de forma segura) y yo:
1. Las agrego al servidor
2. Ejecuto el deployment
3. Verifico que ambos bots estén corriendo
4. Te comparto el acceso a ambos dashboards

---

## ✅ Verificación

Después del deployment, deberías ver:

**Dashboard Bybit:** http://95.216.202.233
**Dashboard Binance:** http://95.216.202.233:8081

Ambos corriendo en dry-run mode (seguro).

---

## ⏱️ Tiempo Estimado

- Crear cuenta: 5 minutos
- KYC: 10-30 minutos (aprobación)
- Crear API: 2 minutos
- **Total: ~20-40 minutos**

---

**¿Listo para crear tu cuenta de Binance?** Avísame cuando tengas las API keys y te ayudo con el deployment! 🚀
