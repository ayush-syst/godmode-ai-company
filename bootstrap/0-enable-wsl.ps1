<#
.SYNOPSIS
    Step 0 of the Godmode AI Company bootstrap (Windows only).
    Enables WSL2 + a Ubuntu distro + (guides) Docker Desktop integration, so the
    rest of the stack can run in Linux where it's happiest.

.DESCRIPTION
    The agent stack (gstack, ruflo, OpenHands, CrewAI, n8n, scanners) targets
    Linux. On Windows 11 the cleanest path is WSL2 + Ubuntu. This script:
      1. Verifies it's running elevated (admin) — required to enable Windows features.
      2. Enables the WSL + Virtual Machine Platform features (idempotent).
      3. Sets WSL default version to 2.
      4. Installs Ubuntu (if not already present).
      5. Checks for Docker Desktop and prints the exact integration steps.
    A reboot is required the first time the Windows features are enabled.

.NOTES
    Run from an ELEVATED PowerShell:  Right-click PowerShell -> "Run as administrator"
    Then:  .\bootstrap\0-enable-wsl.ps1
    Safe to re-run. Honest note: this script does NOT install Docker Desktop
    silently (that needs a GUI installer + your consent) — it links you to it.
#>

#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Distro = "Ubuntu"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg)  { Write-Host "`n=== $msg ===" -ForegroundColor Cyan }
function Write-Ok($msg)    { Write-Host "  [OK] $msg"   -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host "  [!]  $msg"   -ForegroundColor Yellow }
function Write-Info($msg)  { Write-Host "  -    $msg"   -ForegroundColor Gray }

# ── 1. Require elevation ────────────────────────────────────────────────────
$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
    ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Warn "This script must run as Administrator (it enables Windows features)."
    Write-Info "Re-launching elevated... (accept the UAC prompt)"
    try {
        Start-Process -FilePath "powershell.exe" `
            -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Distro $Distro" `
            -Verb RunAs
    } catch {
        Write-Warn "Could not self-elevate. Manually open an admin PowerShell and re-run this file."
    }
    return
}

Write-Step "Godmode AI Company — Step 0: Enable WSL2 + $Distro"
Write-Info "Windows build: $([System.Environment]::OSVersion.Version)"

# ── 2. Fast path: `wsl --install` (Windows 11 / recent Win10) ───────────────
# On modern builds this single command enables features, installs the kernel,
# sets WSL2 default, and installs the distro. We try it first.
$wslAvailable = $null -ne (Get-Command wsl.exe -ErrorAction SilentlyContinue)

$featuresJustEnabled = $false

if ($wslAvailable) {
    Write-Step "Attempting modern install path (wsl --install)"
    try {
        # --no-distribution first so we can pick the distro explicitly afterwards.
        wsl.exe --install --no-distribution
        Write-Ok "WSL core components installed/verified."
    } catch {
        Write-Warn "wsl --install failed; falling back to manual feature enablement."
        $wslAvailable = $false
    }
}

# ── 3. Fallback: enable Windows optional features manually ───────────────────
if (-not $wslAvailable) {
    Write-Step "Enabling Windows features (Microsoft-Windows-Subsystem-Linux + VirtualMachinePlatform)"

    $wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
    if ($wslFeature.State -ne "Enabled") {
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart | Out-Null
        $featuresJustEnabled = $true
        Write-Ok "WSL feature enabled."
    } else { Write-Ok "WSL feature already enabled." }

    $vmFeature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
    if ($vmFeature.State -ne "Enabled") {
        Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart | Out-Null
        $featuresJustEnabled = $true
        Write-Ok "Virtual Machine Platform enabled."
    } else { Write-Ok "Virtual Machine Platform already enabled." }
}

# ── 4. Set WSL2 as the default version ──────────────────────────────────────
Write-Step "Setting WSL default version to 2"
try {
    wsl.exe --set-default-version 2
    Write-Ok "Default WSL version set to 2."
} catch {
    Write-Warn "Could not set WSL2 default yet — usually resolves after a reboot."
}

# ── 5. Reboot gate ──────────────────────────────────────────────────────────
if ($featuresJustEnabled) {
    Write-Step "REBOOT REQUIRED"
    Write-Warn "Windows features were just enabled. Reboot, then RE-RUN this script to install $Distro."
    $answer = Read-Host "  Reboot now? (y/N)"
    if ($answer -eq "y") { Restart-Computer -Force }
    return
}

# ── 6. Install the distro ───────────────────────────────────────────────────
Write-Step "Installing distro: $Distro"
$installed = (wsl.exe --list --quiet) -join "`n"
if ($installed -match [regex]::Escape($Distro)) {
    Write-Ok "$Distro is already installed."
} else {
    Write-Info "Installing $Distro (a username/password prompt will appear in a new window)..."
    wsl.exe --install -d $Distro
    Write-Ok "$Distro install triggered. Complete the first-run user setup in the Ubuntu window."
}

# ── 7. Docker Desktop guidance (not auto-installed by design) ───────────────
Write-Step "Docker Desktop (manual, with consent)"
$dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
if (Test-Path $dockerPath) {
    Write-Ok "Docker Desktop is installed."
    Write-Info "Ensure: Settings -> Resources -> WSL Integration -> enable for '$Distro'."
} else {
    Write-Warn "Docker Desktop not found. OpenHands and n8n run in containers, so install it:"
    Write-Info "  1. Download: https://www.docker.com/products/docker-desktop/"
    Write-Info "  2. During install, keep 'Use WSL 2 instead of Hyper-V' CHECKED."
    Write-Info "  3. After install: Settings -> Resources -> WSL Integration -> enable '$Distro'."
}

# ── 8. Next steps ───────────────────────────────────────────────────────────
Write-Step "Next steps"
Write-Info "1. Open Ubuntu (Start menu -> '$Distro') and finish the user setup if you haven't."
Write-Info "2. In Ubuntu, clone the repo (or cd to it) and run:  bash bootstrap/install.sh"
Write-Info "3. Then:  cp bootstrap/.env.example .env  and fill in your keys."
Write-Ok "Step 0 complete."
