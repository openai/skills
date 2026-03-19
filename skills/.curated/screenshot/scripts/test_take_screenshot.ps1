Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "take_screenshot.ps1"

function Assert-Equal {
  param(
    $Actual,
    $Expected,
    [string]$Message
  )

  if ($Actual -ne $Expected) {
    throw "$Message`nExpected: $Expected`nActual: $Actual"
  }
}

function Assert-True {
  param(
    [bool]$Condition,
    [string]$Message
  )

  if (-not $Condition) {
    throw $Message
  }
}

function Remove-IfExists {
  param([string]$TargetPath)

  if ($TargetPath -and (Test-Path $TargetPath)) {
    Remove-Item -LiteralPath $TargetPath -Force
  }
}

Write-Host "Test 1: explicit path preserves the first display path"
$env:CODEX_SCREENSHOT_TEST_MODE = "1"
$env:CODEX_SCREENSHOT_TEST_DISPLAYS = "1,2"
$explicitBasePath = Join-Path $env:TEMP ("codex-screenshot-explicit-{0}.png" -f [guid]::NewGuid())
$explicitPathOutputs = @(
  & $scriptPath -Path $explicitBasePath
)
Remove-Item Env:CODEX_SCREENSHOT_TEST_MODE
Remove-Item Env:CODEX_SCREENSHOT_TEST_DISPLAYS

try {
  Assert-Equal -Actual $explicitPathOutputs.Count -Expected 2 -Message "Expected one explicit-path output per display"
  Assert-Equal -Actual $explicitPathOutputs[0] -Expected $explicitBasePath -Message "The first display should keep the exact requested path"
  Assert-True -Condition ($explicitPathOutputs[1] -eq [System.IO.Path]::ChangeExtension($explicitBasePath, $null).TrimEnd(".") + "-d2.png") -Message "The second display should use a suffixed sibling path"
} finally {
  foreach ($outputPath in $explicitPathOutputs) {
    Remove-IfExists -TargetPath $outputPath
  }
}

Write-Host "Test 2: empty explicit path falls back to suffixed default outputs"
$env:CODEX_SCREENSHOT_TEST_MODE = "1"
$env:CODEX_SCREENSHOT_TEST_DISPLAYS = "1,2"
$emptyPathOutputs = @(
  & $scriptPath -Mode temp -Path ""
)
Remove-Item Env:CODEX_SCREENSHOT_TEST_MODE
Remove-Item Env:CODEX_SCREENSHOT_TEST_DISPLAYS

try {
  Assert-Equal -Actual $emptyPathOutputs.Count -Expected 2 -Message "Expected one output per display"
  Assert-True -Condition ($emptyPathOutputs[0] -match "-d1\.png$") -Message "Default first display path should be suffixed with -d1 when -Path is empty"
  Assert-True -Condition ($emptyPathOutputs[1] -match "-d2\.png$") -Message "Default second display path should be suffixed with -d2 when -Path is empty"
} finally {
  foreach ($outputPath in $emptyPathOutputs) {
    Remove-IfExists -TargetPath $outputPath
  }
}

Write-Host "Test 3: DPI setup falls back when per-monitor v2 returns false"
$env:CODEX_SCREENSHOT_TEST_MODE = "1"
$env:CODEX_SCREENSHOT_TEST_DISPLAYS = "1,2"
$loadOutputs = @(
  . $scriptPath -Mode temp -VirtualDesktop
)
Remove-Item Env:CODEX_SCREENSHOT_TEST_MODE
Remove-Item Env:CODEX_SCREENSHOT_TEST_DISPLAYS

try {
  Assert-True -Condition ([bool](Get-Command Initialize-DpiAwareness -ErrorAction SilentlyContinue)) -Message "Initialize-DpiAwareness should be available for regression coverage"

  $script:perMonitorCalls = 0
  $script:legacyCalls = 0
  Initialize-DpiAwareness `
    -SetPerMonitorV2 {
      $script:perMonitorCalls++
      return $false
    } `
    -SetLegacyAware {
      $script:legacyCalls++
      return $true
    }

  Assert-Equal -Actual $script:perMonitorCalls -Expected 1 -Message "Per-monitor DPI setup should be attempted once"
  Assert-Equal -Actual $script:legacyCalls -Expected 1 -Message "Legacy DPI setup should run when per-monitor v2 returns false"
} finally {
  foreach ($outputPath in $loadOutputs) {
    Remove-IfExists -TargetPath $outputPath
  }
}

Write-Host "All screenshot regression checks passed."
