# Quick Setup Script - Using Pre-built Freqtrade
# This is faster than cloning the entire repository

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Trading Bot - Quick Setup" -ForegroundColor Cyan
Write-Host "  Using pre-built Freqtrade package" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create virtual environment
Write-Host "[1/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Step 2: Activate and install Freqtrade
Write-Host "[2/5] Installing Freqtrade (this may take a few minutes)..." -ForegroundColor Yellow
& "venv\Scripts\pip.exe" install --upgrade pip
& "venv\Scripts\pip.exe" install freqtrade[all]
Write-Host "  ✓ Freqtrade installed" -ForegroundColor Green
Write-Host ""

# Step 3: Initialize Freqtrade config
Write-Host "[3/5] Initializing Freqtrade directory..." -ForegroundColor Yellow
& "venv\Scripts\freqtrade.exe" create-userdir --userdir user_data
Write-Host "  ✓ User directory created" -ForegroundColor Green
Write-Host ""

# Step 4: Copy strategy and config
Write-Host "[4/5] Copying strategy files..." -ForegroundColor Yellow
Copy-Item "bot_config\GridScalpingHybrid.py" "user_data\strategies\" -Force
Copy-Item "bot_config\config.json" "user_data\" -Force
Copy-Item "bot_config\.env.example" ".env" -Force
Write-Host "  ✓ Strategy and config copied" -ForegroundColor Green
Write-Host ""

# Step 5: Summary
Write-Host "[5/5] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure API Keys:" -ForegroundColor White
Write-Host "   Edit .env file with your Binance API keys" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Activate virtual environment:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Download data for backtesting:" -ForegroundColor White
Write-Host "   freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timerange 20231001-20240101 --timeframe 5m" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Run backtest:" -ForegroundColor White
Write-Host "   freqtrade backtesting --strategy GridScalpingHybrid --timerange 20231001-20240101" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Start paper trading:" -ForegroundColor White
Write-Host "   freqtrade trade --config user_data\config.json --strategy GridScalpingHybrid" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  IMPORTANT: The bot is configured for PAPER TRADING (dry-run mode)" -ForegroundColor Yellow
Write-Host "    No real money will be used until you change dry_run to false" -ForegroundColor Yellow
Write-Host ""
