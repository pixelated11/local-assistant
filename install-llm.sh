#!/bin/bash

echo "Checking for root perms..."
if [ "$EUID" -eq 0 ]; then
    echo "User is on sudo/root."
else
    echo "User is not root. Exiting..."
    exit 1
fi

echo "Checking if Qwen3 4B is already installed..."
if ollama list | grep -q "qwen3:4b"; then
    echo "Qwen3 4B already installed. Redirecting to GUI..."
    exit 0
else
    echo "Qwen3 4B is not installed. Installing now. (Press Ctrl + C to abort)"
fi

echo "Installing Ollama..."
sleep 1

if curl -fsSL https://ollama.com/install.sh | sh; then
    echo "Ollama installed. Pulling Qwen3 4B..."
    ollama pull qwen3:4b
    echo "Done! Redirecting to GUI..."
    exit 0
else
    echo "Installation failed."
    exit 1
fi