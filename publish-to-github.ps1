# GitHub Publishing Script for TeslaMate Integration
# Run this script after installing Git and restarting PowerShell

Write-Host "=== TeslaMate Integration - GitHub Publishing Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if Git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please restart PowerShell after installing Git" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Git is installed" -ForegroundColor Green
Write-Host ""

# Get user information
Write-Host "--- Git Configuration ---" -ForegroundColor Yellow
Write-Host ""

$gitName = Read-Host "Enter your name (for Git commits)"
$gitEmail = Read-Host "Enter your email (for Git commits)"
$githubUsername = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (default: teslamate-hacs)"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "teslamate-hacs"
}

Write-Host ""
Write-Host "--- Configuration Summary ---" -ForegroundColor Cyan
Write-Host "  Name: $gitName"
Write-Host "  Email: $gitEmail"
Write-Host "  GitHub: $githubUsername/$repoName"
Write-Host ""

$confirm = Read-Host "Is this correct? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "[ABORTED]" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[SETUP] Setting up Git..." -ForegroundColor Yellow

# Configure Git
git config --global user.name "$gitName"
git config --global user.email "$gitEmail"
git config --global init.defaultBranch main

Write-Host "[OK] Git configured" -ForegroundColor Green
Write-Host ""

# Initialize repository
Write-Host "[INIT] Initializing Git repository..." -ForegroundColor Yellow
git init

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to initialize repository" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Repository initialized" -ForegroundColor Green
Write-Host ""

# Add all files
Write-Host "[ADD] Adding files..." -ForegroundColor Yellow
git add .

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to add files" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Files added" -ForegroundColor Green
Write-Host ""

# Create initial commit
Write-Host "[COMMIT] Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: TeslaMate Home Assistant Integration v1.0.0"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to create commit" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Initial commit created" -ForegroundColor Green
Write-Host ""

# Add remote
Write-Host "[REMOTE] Adding GitHub remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$githubUsername/$repoName.git"
git remote add origin $remoteUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to add remote" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Remote added: $remoteUrl" -ForegroundColor Green
Write-Host ""

# Create and push main branch
Write-Host "=== Pushing to GitHub ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "[!] IMPORTANT: Before proceeding, make sure you:" -ForegroundColor Yellow
Write-Host "   1. Created a repository on GitHub: $githubUsername/$repoName" -ForegroundColor Yellow
Write-Host "   2. Repository is set to PUBLIC (required for HACS)" -ForegroundColor Yellow
Write-Host ""

$ready = Read-Host "Have you created the GitHub repository? (y/n)"
if ($ready -ne 'y') {
    Write-Host ""
    Write-Host ">> To create the repository:" -ForegroundColor Cyan
    Write-Host "   1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "   2. Repository name: $repoName" -ForegroundColor White
    Write-Host "   3. Description: Complete Home Assistant integration for TeslaMate MQTT" -ForegroundColor White
    Write-Host "   4. Set to PUBLIC" -ForegroundColor White
    Write-Host "   5. Do NOT initialize with README, .gitignore, or license" -ForegroundColor White
    Write-Host "   6. Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    Write-Host "After creating the repository, run this script again." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to push to GitHub" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  1. Repository doesn't exist on GitHub" -ForegroundColor White
    Write-Host "  2. Authentication failed - you may need to set up a Personal Access Token" -ForegroundColor White
    Write-Host "  3. Wrong repository name or username" -ForegroundColor White
    Write-Host ""
    Write-Host "To set up authentication:" -ForegroundColor Cyan
    Write-Host "  1. Go to https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "  2. Generate new token (classic)" -ForegroundColor White
    Write-Host "  3. Select 'repo' scope" -ForegroundColor White
    Write-Host "  4. Use token as password when prompted" -ForegroundColor White
    exit 1
}

Write-Host "[OK] Pushed to GitHub" -ForegroundColor Green
Write-Host ""

# Create release tag
Write-Host "[TAG] Creating release tag v1.0.0..." -ForegroundColor Yellow
git tag -a v1.0.0 -m "Release v1.0.0 - Initial release"
git push origin v1.0.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Failed to push tag (you can do this manually later)" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Release tag created" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== SUCCESS! Your integration is now on GitHub! ===" -ForegroundColor Green
Write-Host ""
Write-Host ">> Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Visit your repository: https://github.com/$githubUsername/$repoName" -ForegroundColor White
Write-Host "  2. Add topics: home-assistant, tesla, teslamate, mqtt, hacs" -ForegroundColor White
Write-Host "  3. Enable Issues and Discussions in Settings" -ForegroundColor White
Write-Host "  4. Update manifest.json with your repo URL" -ForegroundColor White
Write-Host "  5. Add screenshots to README" -ForegroundColor White
Write-Host "  6. Announce on Home Assistant Community" -ForegroundColor White
Write-Host ""
Write-Host "[INFO] For HACS installation, users can add as custom repository:" -ForegroundColor Cyan
Write-Host "   $remoteUrl" -ForegroundColor White
Write-Host ""
Write-Host "*** Congratulations! ***" -ForegroundColor Green
