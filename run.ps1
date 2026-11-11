# Terraform Arena launcher (Windows PowerShell)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt

# Create any missing workspace folders without overwriting your work.
& ".\.venv\Scripts\python.exe" judge.py generate | Out-Host

Write-Host ""
Write-Host "Terraform Arena -> http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
