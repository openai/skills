param(
  [string]$Path,
  [ValidateSet("default", "temp")][string]$Mode = "default",
  [string]$Format = "png",
  [string]$Region,
  [switch]$ActiveWindow,
  [Nullable[Int64]]$WindowHandle,
  [switch]$VirtualDesktop
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$TestModeEnv = "CODEX_SCREENSHOT_TEST_MODE"
$TestDisplaysEnv = "CODEX_SCREENSHOT_TEST_DISPLAYS"
$TestPngBase64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4////fwAJ+wP9KobjigAAAABJRU5ErkJggg=="

function Get-Timestamp {
  Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
}

function Get-DefaultDirectory {
  $userHome = [Environment]::GetFolderPath("UserProfile")
  $pictures = Join-Path $userHome "Pictures"
  $screenshots = Join-Path $pictures "Screenshots"
  if (Test-Path $screenshots) { return $screenshots }
  if (Test-Path $pictures) { return $pictures }
  return $userHome
}

function New-DefaultFilename {
  param([string]$Prefix)
  if (-not $Prefix) { $Prefix = "screenshot" }
  "$Prefix-$(Get-Timestamp).$Format"
}

function Test-ExplicitPathProvided {
  param([string]$CandidatePath)

  return -not [string]::IsNullOrWhiteSpace($CandidatePath)
}

function Resolve-OutputPath {
  if (Test-ExplicitPathProvided -CandidatePath $Path) {
    $expanded = [Environment]::ExpandEnvironmentVariables($Path)
    $homeDir = [Environment]::GetFolderPath("UserProfile")
    if ($expanded -eq "~") {
      $expanded = $homeDir
    } elseif ($expanded.StartsWith("~/") -or $expanded.StartsWith("~\\")) {
      $expanded = Join-Path $homeDir $expanded.Substring(2)
    }
    $full = [System.IO.Path]::GetFullPath($expanded)
    if ((Test-Path $full) -and (Get-Item $full).PSIsContainer) {
      $full = Join-Path $full (New-DefaultFilename "")
    } elseif (($expanded.EndsWith("\") -or $expanded.EndsWith("/")) -and -not (Test-Path $full)) {
      New-Item -ItemType Directory -Path $full -Force | Out-Null
      $full = Join-Path $full (New-DefaultFilename "")
    } elseif ([System.IO.Path]::GetExtension($full) -eq "") {
      $full = "$full.$Format"
    }
    $parent = Split-Path -Parent $full
    if ($parent) {
      New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    return $full
  }

  if ($Mode -eq "temp") {
    $tmp = [System.IO.Path]::GetTempPath()
    return Join-Path $tmp (New-DefaultFilename "codex-shot")
  }

  $dest = Get-DefaultDirectory
  return Join-Path $dest (New-DefaultFilename "")
}

function Parse-Region {
  if (-not $Region) { return $null }
  $parts = $Region.Split(",") | ForEach-Object { $_.Trim() }
  if ($parts.Length -ne 4) {
    throw "Region must be x,y,w,h"
  }
  $values = $parts | ForEach-Object {
    $out = 0
    if (-not [int]::TryParse($_, [ref]$out)) {
      throw "Region values must be integers"
    }
    $out
  }
  if ($values[2] -le 0 -or $values[3] -le 0) {
    throw "Region width and height must be positive"
  }
  return $values
}

function Test-ModeEnabled {
  $value = [Environment]::GetEnvironmentVariable($TestModeEnv)
  if (-not $value) {
    return $false
  }

  return @("1", "true", "yes", "on") -contains $value.ToLowerInvariant()
}

function Get-TestDisplayIds {
  $raw = [Environment]::GetEnvironmentVariable($TestDisplaysEnv)
  if (-not $raw) {
    return @(1, 2)
  }

  $ids = New-Object System.Collections.Generic.List[int]
  foreach ($part in $raw.Split(",")) {
    $value = 0
    if ([int]::TryParse($part.Trim(), [ref]$value)) {
      $ids.Add($value)
    }
  }

  if ($ids.Count -eq 0) {
    return @(1)
  }

  return $ids.ToArray()
}

function New-SuffixedOutputPath {
  param(
    [string]$BasePath,
    [string]$Suffix
  )
  $dir = Split-Path -Parent $BasePath
  if (-not $dir) {
    $dir = "."
  }
  $name = [System.IO.Path]::GetFileNameWithoutExtension($BasePath)
  $ext = [System.IO.Path]::GetExtension($BasePath)
  return Join-Path $dir "$name-$Suffix$ext"
}

function Get-FullScreenOutputPaths {
  param(
    [string]$BasePath,
    [int]$DisplayCount,
    [bool]$PreserveBasePath
  )

  $paths = New-Object System.Collections.Generic.List[string]
  for ($index = 0; $index -lt $DisplayCount; $index++) {
    if ($PreserveBasePath -and $index -eq 0) {
      $paths.Add($BasePath)
      continue
    }

    $paths.Add((New-SuffixedOutputPath -BasePath $BasePath -Suffix ("d{0}" -f ($index + 1))))
  }

  return $paths.ToArray()
}

function Write-TestPng {
  param([string]$DestinationPath)

  $parent = Split-Path -Parent $DestinationPath
  if ($parent) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }

  [System.IO.File]::WriteAllBytes($DestinationPath, [Convert]::FromBase64String($TestPngBase64))
}

function Save-ScreenshotBounds {
  param(
    [System.Drawing.Rectangle]$Bounds,
    [string]$DestinationPath,
    [object]$ImageFormat
  )

  if ($Bounds.Width -le 0 -or $Bounds.Height -le 0) {
    throw "Capture bounds are invalid ($($Bounds.Width)x$($Bounds.Height))"
  }

  $bitmap = New-Object System.Drawing.Bitmap($Bounds.Width, $Bounds.Height)
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  try {
    $source = New-Object System.Drawing.Point($Bounds.Left, $Bounds.Top)
    $target = [System.Drawing.Point]::Empty
    $size = New-Object System.Drawing.Size($Bounds.Width, $Bounds.Height)
    $graphics.CopyFromScreen($source, $target, $size)
    $bitmap.Save($DestinationPath, $ImageFormat)
  } finally {
    $graphics.Dispose()
    $bitmap.Dispose()
  }
}

function Initialize-DpiAwareness {
  param(
    [scriptblock]$SetPerMonitorV2 = { [NativeMethods]::SetProcessDpiAwarenessContext([IntPtr]::new(-4)) },
    [scriptblock]$SetLegacyAware = { [NativeMethods]::SetProcessDPIAware() }
  )

  $perMonitorAware = $false
  try {
    $perMonitorAware = [bool](& $SetPerMonitorV2)
  } catch {
    $perMonitorAware = $false
  }

  if ($perMonitorAware) {
    return
  }

  try {
    & $SetLegacyAware | Out-Null
  } catch {
    # Best effort only; continue when APIs are unavailable.
  }
}

$hasWindowHandle = $PSBoundParameters.ContainsKey("WindowHandle")
$hasExplicitPath = Test-ExplicitPathProvided -CandidatePath $Path

if ($Region -and $ActiveWindow) {
  throw "Choose either -Region or -ActiveWindow"
}
if ($Region -and $hasWindowHandle) {
  throw "Choose either -Region or -WindowHandle"
}
if ($ActiveWindow -and $hasWindowHandle) {
  throw "Choose either -ActiveWindow or -WindowHandle"
}
if ($VirtualDesktop -and ($Region -or $ActiveWindow -or $hasWindowHandle)) {
  throw "-VirtualDesktop only applies to full-screen capture"
}

$regionValues = Parse-Region
$outputPath = Resolve-OutputPath
$testMode = Test-ModeEnabled

if ($testMode) {
  if (-not $regionValues -and -not $ActiveWindow -and -not $hasWindowHandle) {
    $displayIds = Get-TestDisplayIds
    if ($displayIds.Count -gt 1 -and -not $VirtualDesktop) {
      $outputPaths = Get-FullScreenOutputPaths -BasePath $outputPath -DisplayCount $displayIds.Count -PreserveBasePath:$hasExplicitPath
      foreach ($path in $outputPaths) {
        Write-TestPng -DestinationPath $path
        Write-Output $path
      }
      return
    }
  }

  Write-TestPng -DestinationPath $outputPath
  Write-Output $outputPath
  return
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$imageFormat = switch ($Format.ToLowerInvariant()) {
  "png" { [System.Drawing.Imaging.ImageFormat]::Png }
  "jpg" { [System.Drawing.Imaging.ImageFormat]::Jpeg }
  "jpeg" { [System.Drawing.Imaging.ImageFormat]::Jpeg }
  "bmp" { [System.Drawing.Imaging.ImageFormat]::Bmp }
  default { throw "Unsupported format: $Format" }
}

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class NativeMethods {
  [StructLayout(LayoutKind.Sequential)]
  public struct RECT {
    public int Left;
    public int Top;
    public int Right;
    public int Bottom;
  }

  [DllImport("user32.dll")]
  public static extern IntPtr GetForegroundWindow();

  [DllImport("user32.dll")]
  public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

  [DllImport("user32.dll", SetLastError = true)]
  public static extern bool SetProcessDPIAware();

  [DllImport("user32.dll", SetLastError = true)]
  public static extern bool SetProcessDpiAwarenessContext(IntPtr dpiContext);
}
"@

Initialize-DpiAwareness

if ($regionValues) {
  $x = $regionValues[0]
  $y = $regionValues[1]
  $w = $regionValues[2]
  $h = $regionValues[3]
  $bounds = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
} elseif ($ActiveWindow -or $hasWindowHandle) {
  $handle = if ($hasWindowHandle) { [IntPtr]::new([int64]$WindowHandle) } else { [NativeMethods]::GetForegroundWindow() }
  if ($handle -eq [IntPtr]::Zero) {
    throw "No valid window handle found"
  }
  $rect = New-Object NativeMethods+RECT
  if (-not [NativeMethods]::GetWindowRect($handle, [ref]$rect)) {
    throw "Failed to get window bounds"
  }
  $width = $rect.Right - $rect.Left
  $height = $rect.Bottom - $rect.Top
  if ($width -le 0 -or $height -le 0) {
    throw "Window bounds are invalid; make sure the window is visible and not minimized"
  }
  $bounds = New-Object System.Drawing.Rectangle($rect.Left, $rect.Top, $width, $height)
} else {
  $screens = [System.Windows.Forms.Screen]::AllScreens
  if ($screens.Count -gt 1 -and -not $VirtualDesktop) {
    $outputPaths = Get-FullScreenOutputPaths -BasePath $outputPath -DisplayCount $screens.Count -PreserveBasePath:$hasExplicitPath
    $savedPaths = New-Object System.Collections.Generic.List[string]
    for ($index = 0; $index -lt $screens.Count; $index++) {
      $screen = $screens[$index]
      $screenBounds = $screen.Bounds
      if ($screenBounds.Width -le 0 -or $screenBounds.Height -le 0) {
        continue
      }
      $displayPath = $outputPaths[$index]
      Save-ScreenshotBounds -Bounds $screenBounds -DestinationPath $displayPath -ImageFormat $imageFormat
      $savedPaths.Add($displayPath)
    }

    if ($savedPaths.Count -eq 0) {
      throw "Failed to capture any display; verify that monitors are active"
    }

    $savedPaths | ForEach-Object { Write-Output $_ }
    return
  }

  $vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
  $bounds = New-Object System.Drawing.Rectangle($vs.Left, $vs.Top, $vs.Width, $vs.Height)
}

Save-ScreenshotBounds -Bounds $bounds -DestinationPath $outputPath -ImageFormat $imageFormat

Write-Output $outputPath
