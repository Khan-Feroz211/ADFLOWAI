# ADFLOWAI - Check status of all services
Clear-Host
Write-Host ""
Write-Host "  ADFLOWAI - Service Status" -ForegroundColor Cyan
Write-Host ""

docker-compose ps

Write-Host ""
Write-Host "  Testing endpoints..." -ForegroundColor Cyan

# Test API
try {
    $r = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  ✓ API:      http://localhost:5000  [HEALTHY]" -ForegroundColor Green
} catch {
    Write-Host "  ✗ API:      http://localhost:5000  [NOT RESPONDING]" -ForegroundColor Red
}

# Test Frontend
try {
    $r = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  ✓ Frontend: http://localhost:3000  [RUNNING]" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Frontend: http://localhost:3000  [NOT RESPONDING]" -ForegroundColor Red
}

# Test Flower
try {
    $r = Invoke-WebRequest -Uri "http://localhost:5555" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  ✓ Flower:   http://localhost:5555  [RUNNING]" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Flower:   http://localhost:5555  [NOT RESPONDING]" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to close"
