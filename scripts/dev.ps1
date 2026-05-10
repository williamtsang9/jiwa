Param(
    [string]$HostName = "127.0.0.1",
    [int]$Port = 3000
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Pip = Join-Path $Root ".venv\Scripts\pip.exe"

& $Pip install -r requirements.txt | Out-Host

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

$env:APP_HOST = $HostName
$env:APP_PORT = "$Port"

$hasWt = $null -ne (Get-Command wt -ErrorAction SilentlyContinue)

if ($hasWt) {
    wt `
      -w 0 nt --title "jiwa-app" powershell -NoExit -Command "cd '$Root'; .\.venv\Scripts\Activate.ps1; python app.py" `
      ; split-pane -V -p 40 powershell -NoExit -Command "cd '$Root'; if (!(Test-Path 'logs\falcon.log')) { New-Item -ItemType File -Path 'logs\falcon.log' | Out-Null }; Get-Content -Path 'logs\falcon.log' -Wait" `
      ; split-pane -H -p 50 powershell -NoExit -Command "cd '$Root'; .\.venv\Scripts\Activate.ps1; while (`$true) { pytest -q; Start-Sleep -Seconds 3 }" `
      ; focus-pane -t 0

    Write-Host "Dev layout launched in Windows Terminal."
    Write-Host "App URL: http://$HostName`:$Port"
    exit 0
}

Write-Host "Windows Terminal not found. Starting background processes in this shell."
Write-Host "App URL: http://$HostName`:$Port"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; .\.venv\Scripts\Activate.ps1; python app.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; if (!(Test-Path 'logs\falcon.log')) { New-Item -ItemType File -Path 'logs\falcon.log' | Out-Null }; Get-Content -Path 'logs\falcon.log' -Wait"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; .\.venv\Scripts\Activate.ps1; while (`$true) { pytest -q; Start-Sleep -Seconds 3 }"
