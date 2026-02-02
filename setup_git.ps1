# Git Setup para Trading Bot

# Crear .gitignore si no existe
if (!(Test-Path .gitignore)) {
    Write-Host "Creating .gitignore..." -ForegroundColor Yellow
    Copy-Item .gitignore.example .gitignore -ErrorAction SilentlyContinue
}

# Inicializar Git
if (!(Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "Git repository already initialized" -ForegroundColor Green
}

# Verificar que archivos sensibles no se subirán
Write-Host "`nVerifying .gitignore..." -ForegroundColor Yellow
$gitignoreContent = Get-Content .gitignore -Raw
$sensitiveFiles = @(".env", "*.sqlite", "*.db")

foreach ($file in $sensitiveFiles) {
    if ($gitignoreContent -notmatch [regex]::Escape($file)) {
        Write-Host "  ⚠️  Warning: $file not in .gitignore!" -ForegroundColor Red
    } else {
        Write-Host "  ✅ $file is protected" -ForegroundColor Green
    }
}

# Agregar archivos
Write-Host "`nAdding files to Git..." -ForegroundColor Yellow
git add .

# Status
Write-Host "`nGit Status:" -ForegroundColor Cyan
git status

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "  Git Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host ""
Write-Host "1. Review files to commit:" -ForegroundColor Yellow
Write-Host "   git status" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Make initial commit:" -ForegroundColor Yellow
Write-Host "   git commit -m 'Initial trading bot setup'" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Create GitHub repository:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com/new" -ForegroundColor Gray
Write-Host "   - Name: trading-bot" -ForegroundColor Gray
Write-Host "   - Private: Yes (recommended)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Connect to GitHub:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/YOUR-USERNAME/trading-bot.git" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Push to GitHub:" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Deploy in Easypanel:" -ForegroundColor Yellow
Write-Host "   - Connect GitHub repository" -ForegroundColor Gray
Write-Host "   - See EASYPANEL_DEPLOYMENT.md for details" -ForegroundColor Gray
Write-Host ""
