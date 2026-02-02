# 📋 Instrucciones para Conectar GitHub

## ✅ Lo que ya hice:
- ✅ Inicialicé Git
- ✅ Agregué todos los archivos
- ✅ Hice el primer commit
- ✅ Creé la rama `main`

---

## 🔗 Lo que TÚ necesitas hacer (2 minutos):

### Paso 1: Crear Repositorio en GitHub

1. **Ir a GitHub**:
   - https://github.com/new

2. **Configurar repo**:
   ```
   Repository name: trading-bot
   Description: Trading bot automatizado con GridScalpingHybrid
   Private: ✅ (RECOMENDADO - para proteger tus estrategias)
   ```

3. **NO marcar**:
   - ❌ Add README
   - ❌ Add .gitignore  
   - ❌ Add license
   
   (Ya tenemos todo esto)

4. **Click "Create repository"**

---

### Paso 2: Conectar y Subir

Después de crear el repo, GitHub te mostrará comandos. **Usa estos**:

```powershell
# En tu terminal de PowerShell:
cd C:\Users\guido\OneDrive\G2INNOVATION\TRADING_AUTOMATICO

# Conectar con tu repositorio (reemplaza TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/trading-bot.git

# Subir el código
git push -u origin main
```

**Ejemplo**:
Si tu usuario de GitHub es `guidog2innovation`:
```powershell
git remote add origin https://github.com/guidog2innovation/trading-bot.git
git push -u origin main
```

---

### Paso 3: Autenticación

Si te pide usuario/contraseña:

**Opción A**: Usar Personal Access Token (recomendado)
1. Ir a: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `trading-bot-deploy`
4. Scopes: marcar `repo` (todo)
5. Click "Generate token"
6. **COPIAR EL TOKEN** (se muestra solo una vez)
7. Cuando git pida password, pegar el token

**Opción B**: Usar GitHub CLI
```powershell
# Instalar GitHub CLI
winget install GitHub.cli

# Autenticarse
gh auth login
```

---

## 🎯 Para Easypanel

Una vez que el código esté en GitHub:

### 1. En Easypanel → New App

**Source**:
- Type: `GitHub`
- Repository: `TU-USUARIO/trading-bot`
- Branch: `main`

**Build**:
- Build Method: `Dockerfile`
- Dockerfile Path: `./Dockerfile`

**Environment Variables** (copy-paste):
```env
EXCHANGE_API_KEY=xYRBUDX0k7Fu9xV2dFO7SJHIRnlpJ5jlUPS1O8dMOgDBf9xMt0osJAMkmbeym5lC
EXCHANGE_SECRET=Xl5zoTZbqQ0pGCwZZBeL0yQTaOkiZQj8Xt6J67Nh2Xc1xhA8VDzruxDBZdXl7S5N
DRY_RUN=true
INITIAL_CAPITAL=1000
MAX_OPEN_TRADES=5
STAKE_AMOUNT=100
```

**Resources** (recomendado):
- Memory: `512MB` (mínimo) o `1GB` (mejor)
- CPU: `0.5 cores`

**Restart Policy**:
- `Always`

---

## 📊 Verificación

Después de deploy en Easypanel:

1. **Ver logs**:
   - Easypanel → Tu App → Logs
   - Deberías ver: `Freqtrade successfully loaded`

2. **Verificar trades**:
   - Logs mostrarán señales de compra/venta
   - En dry_run, no hay dinero real

3. **Monitorear**:
   - Revisar logs daily
   - Ver performance del bot

---

## ❓ Ayuda Rápida

**Error al push**:
```powershell
# Si ya existe el remote
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/trading-bot.git
git push -u origin main
```

**Actualizar código después**:
```powershell
git add .
git commit -m "Descripción del cambio"
git push
# Easypanel desplegará automáticamente!
```

---

## 🎉 ¡Listo!

Una vez que:
- ✅ Código esté en GitHub
- ✅ Easypanel desplegado
- ✅ Logs muestren bot funcionando

**El bot estará corriendo 24/7 en la nube! 🚀**
