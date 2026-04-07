# PowerShell Script for installing Ollama on user's machine. Must be run as administrator.
# Auto-elevate to admin if not already
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requesting admin privileges..."
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs -Wait
    exit
}

Write-Host "Checking for admin perms..."
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "User is not admin. Exiting..."
    exit 1
}
Write-Host "User is admin."

Write-Host "Checking if Qwen3 4B is already installed..."
$ollamaList = ollama list 2>&1
if ($ollamaList -match "qwen3:4b-q4_K_M") {
    Write-Host "Qwen3 4B already installed. Redirecting to GUI..."
    exit 0
} else {
    Write-Host "Qwen3 4B is not installed. Installing now. (Press Ctrl+C to abort)"
}

Write-Host "Installing Ollama..."
Start-Sleep -Seconds 1

# Download and run Ollama installer
$installerUrl = "https://ollama.com/download/OllamaSetup.exe"
$installerPath = "$env:TEMP\OllamaSetup.exe"

Write-Host "Downloading Ollama installer..."
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

Write-Host "Running Ollama installer..."
Start-Process -FilePath $installerPath -ArgumentList "/silent" -Wait

if ($LASTEXITCODE -eq 0) {
    Write-Host "Ollama installed. Pulling Qwen3 4B..."
    ollama pull qwen3:4b-q4_K_M
    Write-Host "Done! Redirecting to GUI..."
    exit 0
} else {
    Write-Host "Installation failed."
    exit 1
}