param(
    [ValidateSet('start', 'test')]
    [string]$Action = 'start'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw 'Create .venv first; see docs/development.md.'
}

if ($Action -eq 'start') {
    $envFile = Join-Path $projectRoot '.env'
    if (Test-Path -LiteralPath $envFile) {
        foreach ($line in Get-Content -LiteralPath $envFile) {
            if ($line -match '^\s*(HELPDESK_URL|HELPDESK_TOKEN)=(.*)$') {
                [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim(), 'Process')
            }
        }
    }
}

Push-Location (Join-Path $projectRoot 'app')
try {
    if ($Action -eq 'test') {
        & $python -m pytest -q
    } else {
        & $python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
    }
    $result = $LASTEXITCODE
} finally {
    Pop-Location
}
exit $result
