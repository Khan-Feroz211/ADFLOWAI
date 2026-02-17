# ADFLOWAI - Stop all services
Write-Host "Stopping ADFLOWAI..." -ForegroundColor Yellow
docker-compose down
Write-Host "All services stopped." -ForegroundColor Green
Read-Host "Press Enter to close"
