# ADFLOWAI - GitHub Push Script (PowerShell)
# Run this in VS Code terminal to push everything to GitHub

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ADFLOWAI - Pushing to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Check git is installed ───────────────────────
try {
    git --version | Out-Null
    Write-Host "[OK] Git is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git not installed! Download from https://git-scm.com" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# ── Step 2: Configure git (edit these!) ──────────────────
$gitName  = "Khan Feroz"
$gitEmail = "khan.feroz@example.com"   # <-- change to your real email
$repoUrl  = "https://github.com/Khan-Feroz211/ADFLOWAI.git"

git config --global user.name  $gitName
git config --global user.email $gitEmail
Write-Host "[OK] Git configured as: $gitName <$gitEmail>" -ForegroundColor Green

# ── Step 3: Init repo if not already ─────────────────────
if (-not (Test-Path ".git")) {
    git init
    git branch -M main
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Git repository already exists" -ForegroundColor Green
}

# ── Step 4: Set remote ────────────────────────────────────
$remotes = git remote 2>&1
if ($remotes -match "origin") {
    git remote set-url origin $repoUrl
    Write-Host "[OK] Remote URL updated" -ForegroundColor Green
} else {
    git remote add origin $repoUrl
    Write-Host "[OK] Remote added: $repoUrl" -ForegroundColor Green
}

# ── Step 5: Add all files ─────────────────────────────────
Write-Host ""
Write-Host "[..] Adding files..." -ForegroundColor Yellow
git add .

# Show what will be committed
$status = git status --short
Write-Host ""
Write-Host "Files to commit:" -ForegroundColor Cyan
git status --short
Write-Host ""

# ── Step 6: Commit ────────────────────────────────────────
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$message   = "ADFLOWAI platform - React frontend + auth + AI engine [$timestamp]"

git commit -m $message
Write-Host "[OK] Committed: $message" -ForegroundColor Green

# ── Step 7: Push ──────────────────────────────────────────
Write-Host ""
Write-Host "[..] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "     You may be asked for your GitHub credentials." -ForegroundColor Gray
Write-Host "     Username: Khan-Feroz211" -ForegroundColor Gray
Write-Host "     Password: Use your Personal Access Token (NOT your password)" -ForegroundColor Gray
Write-Host "     Get token at: https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  View your repo at:" -ForegroundColor Cyan
    Write-Host "  https://github.com/Khan-Feroz211/ADFLOWAI" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERROR] Push failed. Common fixes:" -ForegroundColor Red
    Write-Host "  1. Make sure repo exists at: $repoUrl" -ForegroundColor Yellow
    Write-Host "  2. Use Personal Access Token as password (not your GitHub password)" -ForegroundColor Yellow
    Write-Host "  3. Get token at: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host "  4. If repo has existing files: run 'git pull origin main --rebase' first" -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Press Enter to close"
