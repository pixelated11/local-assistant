#!/bin/bash

echo "Checking for root perms..."
if [ "$EUID" -eq 0 ]; then
    echo "User is on sudo/root."
else
    echo "User is not root. Exiting..."
    exit 1
fi

echo "Checking if Ollama (for Llama 3-8B) exists..."
if [ -d /usr/local/lib/ollama ]; then
    echo "Llama 3-8B exists. Installation not needed. Exiting..."
    exit 0
else
    echo "Llama 3-8B is not installed. Installing now. (Press Ctrl + C to abort)"
fi

echo "Installing Llama 3-8B..."
sleep 1

if curl -fsSL https://ollama.com/install.sh | sh; then
    echo "Llama 3-8B installation using Ollama succeeded. Redirecting to GUI..."
    python program.py
    exit 0
else
    echo "Llama 3-8B installation using Ollama failed. Cannot continue local-LLM installation."
    exit 1
fi