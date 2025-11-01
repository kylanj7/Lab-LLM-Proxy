#!/bin/bash

# Ensure Ollama is running
if ! systemctl is-active --quiet ollama; then
    echo "Ollama is not running. Starting Ollama..."
    sudo systemctl start ollama
fi

# Install required packages if not already installed
pip install flask requests

# Use the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run the proxy server
python3 ollama_proxy.py
