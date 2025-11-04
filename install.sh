#!/bin/bash
# Lab-vLLM-Server Installation Script

echo "Installing Lab-LLM-Server..."

# Create directory structure
mkdir -p ~/Lab-LLM-Server

# Make sure Ollama is running (if installed)
if command -v systemctl &> /dev/null && systemctl is-active --quiet ollama; then
    echo "Ollama is running"
elif command -v ollama &> /dev/null; then
    echo "Starting Ollama..."
    # For non-systemd systems or manual installation
    ollama serve &
else
    echo "Warning: Ollama not found. Please install Ollama first:"
    echo "Visit https://ollama.com/download for installation instructions."
fi

# Install required packages
echo "Installing Python dependencies..."
pip install flask requests werkzeug

# Clone repository if it doesn't exist
if [ ! -d "Lab-LLM-Server" ]; then
    echo "Cloning repository..."
    git clone https://github.com/kylanj7/Lab-LLM-Proxy.git Lab-vLLM-Server
    cd Lab-LLM-Server
else
    echo "Repository already exists, updating..."
    cd Lab-LLM-Server
    git pull origin main
fi

echo "Lab-Server has been installed to ~/Lab-LLM-Server/"
echo ""
echo "To start the server, run:"
echo "cd ~/Lab-LLM-Server && python ollama_proxy.py"
echo ""
echo "Then visit http://localhost:8080 in your browser."
echo ""
echo "Default login credentials:"
echo "Username: Kylan"
echo "Password: password1"
