@echo off
REM ADFLOWAI - Windows Quick Start
REM Run this from the ADFLOWAI-VSCODE folder in PowerShell or CMD

echo.
echo  ==========================================
echo    ADFLOWAI - Starting Development Stack
echo  ==========================================
echo.

REM Step 1: Check Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Step 2: Stop any existing containers
echo [..] Stopping existing containers...
docker-compose down 2>nul

REM Step 3: Build images
echo [..] Building Docker images (first time takes 2-3 minutes)...
docker-compose build
if %errorlevel% neq 0 (
    echo [ERROR] Build failed! Check error messages above.
    pause
    exit /b 1
)
echo [OK] Images built

REM Step 4: Start services
echo [..] Starting all services...
docker-compose up -d
if %errorlevel% neq 0 (
    echo [ERROR] Could not start services!
    pause
    exit /b 1
)

REM Step 5: Wait for services to be ready
echo [..] Waiting for database to be ready (15 seconds)...
timeout /t 15 /nobreak >nul

REM Step 6: Check status
echo.
echo  Service Status:
docker-compose ps

echo.
echo  ==========================================
echo    ADFLOWAI is Running!
echo  ==========================================
echo.
echo   API:          http://localhost:5000
echo   Health check: http://localhost:5000/health
echo   Flower:       http://localhost:5555
echo.
echo   Test with:
echo   curl http://localhost:5000/health
echo.
echo   Register a user:
echo   curl -X POST http://localhost:5000/api/v1/auth/register ^
echo     -H "Content-Type: application/json" ^
echo     -d "{\"username\":\"admin\",\"email\":\"admin@test.com\",\"password\":\"Admin123!\"}"
echo.
echo   To stop: docker-compose down
echo   To view logs: docker-compose logs -f api
echo.
pause
