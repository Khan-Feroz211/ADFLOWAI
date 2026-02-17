# ============================================================
#  ADFLOWAI - ONE-CLICK COMPLETE SETUP
#  Run this once and everything works automatically
#  Right-click → "Run with PowerShell"  OR  .\SETUP.ps1
# ============================================================

$ErrorActionPreference = "Stop"

function Write-Step($msg)  { Write-Host "`n[$msg]" -ForegroundColor Cyan }
function Write-OK($msg)    { Write-Host "  ✓ $msg" -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host "  ! $msg" -ForegroundColor Yellow }
function Write-Fail($msg)  { Write-Host "  ✗ $msg" -ForegroundColor Red }

Clear-Host
Write-Host ""
Write-Host "  ╔══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║        ADFLOWAI SETUP v4.0           ║" -ForegroundColor Cyan
Write-Host "  ║   AI-Powered Campaign Optimizer      ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Check we're in the right folder ──────────────────────────
Write-Step "Checking location"
if (-not (Test-Path "app.py")) {
    Write-Fail "app.py not found! Make sure you're in the ADFLOWAI-VSCODE folder"
    Write-Host "  Run: cd 'C:\Users\Feroz Khan\Downloads\ADFLOWAI-VSCODE'" -ForegroundColor Yellow
    Read-Host "`nPress Enter to exit"
    exit 1
}
Write-OK "In correct folder: $(Get-Location)"

# ── Check Docker ──────────────────────────────────────────────
Write-Step "Checking Docker"
try {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Docker not running" }
    Write-OK "Docker is running"
} catch {
    Write-Fail "Docker is not running!"
    Write-Host "  Please start Docker Desktop first, then run this script again" -ForegroundColor Yellow
    Read-Host "`nPress Enter to exit"
    exit 1
}

# ── Stop old containers ───────────────────────────────────────
Write-Step "Stopping old containers"
docker-compose down --remove-orphans 2>&1 | Out-Null
Write-OK "Old containers stopped"

# ── Build images ──────────────────────────────────────────────
Write-Step "Building Docker images (3-5 minutes first time...)"
Write-Warn "Please wait, downloading and installing everything..."
$buildResult = docker-compose build --no-cache 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Build failed! Error:"
    Write-Host $buildResult -ForegroundColor Red
    Read-Host "`nPress Enter to exit"
    exit 1
}
Write-OK "All images built successfully"

# ── Start services ────────────────────────────────────────────
Write-Step "Starting all services"
$upResult = docker-compose up -d 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to start services:"
    Write-Host $upResult -ForegroundColor Red
    Read-Host "`nPress Enter to exit"
    exit 1
}
Write-OK "All containers started"

# ── Wait for API to be ready ──────────────────────────────────
Write-Step "Waiting for API to be ready"
$maxWait  = 60
$interval = 3
$elapsed  = 0
$ready    = $false

while ($elapsed -lt $maxWait) {
    Start-Sleep -Seconds $interval
    $elapsed += $interval
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {}
    Write-Host "  Waiting... ($elapsed/$maxWait seconds)" -ForegroundColor Gray
}

if (-not $ready) {
    Write-Warn "API taking longer than expected - checking logs..."
    docker-compose logs api --tail=20
} else {
    Write-OK "API is ready!"
}

# ── Wait for frontend ─────────────────────────────────────────
Write-Step "Waiting for Frontend (npm install runs first time...)"
Write-Warn "Frontend takes 2-3 minutes on first run"
$elapsed = 0
$ready   = $false

while ($elapsed -lt 180) {
    Start-Sleep -Seconds 5
    $elapsed += 5
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {}
    if ($elapsed % 15 -eq 0) {
        Write-Host "  Still loading... ($elapsed seconds)" -ForegroundColor Gray
    }
}

if ($ready) {
    Write-OK "Frontend is ready!"
} else {
    Write-Warn "Frontend still loading - open http://localhost:3000 in a minute"
}

# ── Container status ──────────────────────────────────────────
Write-Step "Container Status"
docker-compose ps

# ── Push to GitHub ────────────────────────────────────────────
Write-Step "Pushing to GitHub"
try {
    git add . 2>&1 | Out-Null
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "ADFLOWAI v4 - Admin fix, reports, CI/CD [$timestamp]" 2>&1 | Out-Null
    git push origin main 2>&1 | Out-Null
    Write-OK "Pushed to GitHub successfully"
} catch {
    Write-Warn "GitHub push skipped - run push_to_github.ps1 separately if needed"
}

# ── Done! ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ╔══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║          ADFLOWAI IS RUNNING! 🚀             ║" -ForegroundColor Green
Write-Host "  ╠══════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "  ║                                              ║" -ForegroundColor Green
Write-Host "  ║   Frontend:   http://localhost:3000          ║" -ForegroundColor Green
Write-Host "  ║   API:        http://localhost:5000          ║" -ForegroundColor Green
Write-Host "  ║   API Health: http://localhost:5000/health   ║" -ForegroundColor Green
Write-Host "  ║   Flower:     http://localhost:5555          ║" -ForegroundColor Green
Write-Host "  ║                                              ║" -ForegroundColor Green
Write-Host "  ╠══════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "  ║  NEXT STEPS:                                 ║" -ForegroundColor Cyan
Write-Host "  ║  1. Open http://localhost:3000 in browser    ║" -ForegroundColor Cyan
Write-Host "  ║  2. Register your account                    ║" -ForegroundColor Cyan
Write-Host "  ║  3. Go to /admin → click Make Me Admin       ║" -ForegroundColor Cyan
Write-Host "  ║  4. Start creating campaigns!                ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Open browser automatically
Start-Process "http://localhost:3000"

Read-Host "Press Enter to close"
