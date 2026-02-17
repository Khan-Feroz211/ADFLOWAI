# ============================================================
#  ADFLOWAI - UPDATE SCRIPT
#  Run when you download a new version
#  Right-click → "Run with PowerShell"
# ============================================================

$ErrorActionPreference = "Continue"

function Write-Step($msg) { Write-Host "`n[$msg]" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "  ✓ $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  ! $msg" -ForegroundColor Yellow }

Clear-Host
Write-Host ""
Write-Host "  ADFLOWAI - Applying Update" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "app.py")) {
    Write-Host "  ERROR: Run this from inside ADFLOWAI-VSCODE folder!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Stop containers
Write-Step "Stopping services"
docker-compose down 2>&1 | Out-Null
Write-OK "Stopped"

# Rebuild only what changed
Write-Step "Rebuilding (faster than first time)"
docker-compose build 2>&1 | Out-Null
Write-OK "Built"

# Restart
Write-Step "Starting services"
docker-compose up -d 2>&1 | Out-Null
Write-OK "Started"

# Wait for health
Write-Step "Waiting for API..."
Start-Sleep -Seconds 15
try {
    $r = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-OK "API is healthy"
} catch {
    Write-Warn "API still starting - wait 30 more seconds then open http://localhost:3000"
}

Write-Host ""
Write-Host "  Update complete! Open http://localhost:3000" -ForegroundColor Green
Write-Host ""
Start-Process "http://localhost:3000"
Read-Host "Press Enter to close"
