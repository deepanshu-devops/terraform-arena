# Install the Terraform CLI locally (no admin rights required).
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\install_terraform.ps1
param(
    [string]$Version = "1.9.8"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$tools = Join-Path $root "tools"
$target = Join-Path $tools "terraform"
New-Item -ItemType Directory -Force -Path $tools | Out-Null

$arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "386" }
$zip = Join-Path $env:TEMP "terraform_$Version.zip"
$url = "https://releases.hashicorp.com/terraform/$Version/terraform_${Version}_windows_$arch.zip"

Write-Host "Downloading $url" -ForegroundColor Cyan
Invoke-WebRequest -Uri $url -OutFile $zip

if (Test-Path $target) { Remove-Item -Recurse -Force $target }
Expand-Archive -Path $zip -DestinationPath $target -Force
Remove-Item $zip -Force

$exe = Join-Path $target "terraform.exe"
if (-not (Test-Path $exe)) {
    throw "terraform.exe was not extracted."
}

Write-Host ""
& $exe version
Write-Host ""
Write-Host "Installed at: $exe" -ForegroundColor Green
Write-Host "Add it to your PATH for this session:" -ForegroundColor Yellow
Write-Host "  `$env:Path = `"$target;`$env:Path`""
Write-Host ""
Write-Host "Then enable live validation when launching the app:"
Write-Host "  `$env:ARENA_TERRAFORM = '1'"
Write-Host "  .\run.ps1"
