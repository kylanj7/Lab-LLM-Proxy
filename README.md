BETA TESTING PHASE

# Ollama Proxy Server
Running 5 simultaneous sessions with each user selecting LLama3.2:3b local.  

<img width="3223" height="2102" alt="Screenshot from 2025-10-31 18-13-40" src="https://github.com/user-attachments/assets/5df60658-099b-4419-ad00-d5ed8d8551d7" />

A simple web interface and API proxy for interacting with Ollama's local LLM server.
Will run 
## Overview

This project provides a Flask-based web server that acts as a proxy between users and a locally running Ollama instance. It offers:

- A clean web interface for sending prompts to Ollama models
- Basic authentication for multiple users
- API endpoints for generating text and listing available models

## Requirements

- Python 3.6+
- Flask
- Requests
- Ollama installed and running on the same machine

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ollama-proxy.git
   cd ollama-proxy
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure Ollama is installed and running:
   ```bash
   # Check if Ollama is running
   systemctl is-active --quiet ollama || sudo systemctl start ollama
   ```

## Usage

### Running the server

Start the server with default settings (host 0.0.0.0, port 8080):
```bash
python ollama_proxy.py
```

Or with custom settings:
```bash
python ollama_proxy.py --host 127.0.0.1 --port 5000
```

### Accessing the web interface

Open a browser and navigate to:
```
http://localhost:8080/?username=USERNAME&password=PASSWORD
```

Replace `USERNAME` and `PASSWORD` with valid credentials from the predefined user list.

### API Endpoints

#### Generate text
```
POST /generate
```
Headers:
- Content-Type: application/json
- Authorization: Basic base64(username:password)

Body:
```json
{
  "prompt": "Your prompt text here",
  "model": "model_name"
}
```



#### List available models
```
GET /models
```
Headers:
- Authorization: Basic base64(username:password)

## Authentication

The server uses basic authentication. Users are currently defined in the `USERS` dictionary in the script. For production use, it's recommended to implement a more secure authentication system.

## Security Considerations

- Current authentication is basic and stores passwords in plain text
- For production use, consider:
  - Using environment variables for credentials
  - Implementing proper password hashing
  - Adding HTTPS support
  - Restricting access to trusted networks

## License

[Specify your license here]
