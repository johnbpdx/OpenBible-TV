# deploy.ps1 - Build and sideload OpenBible-TV to Roku
# Usage: .\deploy.ps1
# Or with overrides: .\deploy.ps1 -RokuHost 192.168.0.5 -Password mypassword
#
# Credentials are read from ../.env (gitignored).
# Copy ../.env.example to ../.env and fill in your values.

param(
    [string]$RokuHost = "",
    [string]$Password = ""
)

$ErrorActionPreference = "Stop"

# Load .env if it exists
$envFile = Join-Path $PSScriptRoot "../.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
            $name = $Matches[1].Trim()
            $value = $Matches[2].Trim()
            if (-not [System.Environment]::GetEnvironmentVariable($name)) {
                [System.Environment]::SetEnvironmentVariable($name, $value)
            }
        }
    }
}

# Resolve from env if not passed as params
if ($RokuHost -eq "") { $RokuHost = $env:ROKU_HOST }
if ($Password -eq "")  { $Password  = $env:ROKU_PASSWORD }

if (-not $RokuHost -or -not $Password) {
    Write-Host "ERROR: ROKU_HOST and ROKU_PASSWORD must be set in .env or passed as parameters." -ForegroundColor Red
    Write-Host "Copy .env.example to .env and fill in your Roku's IP and developer password."
    exit 1
}

# Step 1: Build
Write-Host "Building with BrighterScript..." -ForegroundColor Cyan
npx bsc
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

$zipPath = Resolve-Path "out/roku.zip"
Write-Host "Built: $zipPath" -ForegroundColor Green

# Step 2: Deploy via curl (handles HTTP Digest auth reliably)
Write-Host "Deploying to Roku at $RokuHost ..." -ForegroundColor Cyan

$result = curl.exe --digest --silent --show-error `
    -u "rokudev:$Password" `
    -F "mysubmit=Install" `
    -F "archive=@$zipPath" `
    "http://$RokuHost/plugin_install"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Deploy failed." -ForegroundColor Red
    Write-Host $result
    exit 1
}

if ($result -match "Install Success") {
    Write-Host "Deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "Deploy response:" -ForegroundColor Yellow
    Write-Host $result
}
