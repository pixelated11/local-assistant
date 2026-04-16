param (
    [string]$Model = "qwen3:4b"
)

# Auto-elevate to admin
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requesting admin privileges..."
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`" -Model `"$Model`"" -Verb RunAs -Wait
    exit
}
Write-Host "User is admin."

Write-Host "Checking if $Model is already installed..."
$ollamaList = ollama list 2>&1
if ($ollamaList -match [regex]::Escape($Model)) {
    Write-Host "$Model already installed. Redirecting to GUI..."
    exit 0
} else {
    Write-Host "$Model is not installed. Installing now. (Press Ctrl+C to abort)"
}

Write-Host "Installing Ollama..."
Start-Sleep -Seconds 1

$installerUrl = "https://ollama.com/download/OllamaSetup.exe"
$installerPath = "$env:TEMP\OllamaSetup.exe"

Write-Host "Downloading Ollama installer..."
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

Write-Host "Running Ollama installer..."
Start-Process -FilePath $installerPath -ArgumentList "/silent" -Wait

if ($LASTEXITCODE -eq 0) {
    Write-Host "Ollama installed. Pulling $Model..."
    ollama pull $Model
    Write-Host "Done! Redirecting to GUI..."
    exit 0
} else {
    Write-Host "Installation failed."
    exit 1
}