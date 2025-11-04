# Lab-LLM-Proxy

Fast Local GPU inference for 5+ users (under 15 seconds) using the llama3.2:3b model. Server SPECS: 3090ti (24GB VRAM), Epyc 7302 & 128GB DDR4 @ 2666MT/s 1Gb small home network

<img width="3223" height="2102" alt="Screenshot from 2025-10-31 18-13-51" src="https://github.com/user-attachments/assets/ccdea431-b3e8-4295-8487-3484eb80a7dc" />

A simple web interface and API proxy for interacting with Ollama's local LLM server, featuring secure authentication.

## Overview

This project provides a Flask-based web server that acts as a proxy between users and a locally running Ollama instance. It offers:

- A clean web interface for sending prompts to Ollama models
- Secure user authentication with login page and password hashing
- Session management for browser-based access
- API endpoints for generating text and listing available models
- Support for both web browser and API authentication methods

## Requirements

- Python 3.6+
- Flask
- Requests
- Werkzeug (for password hashing)
- Ollama installed and running on the same machine

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kylanj7/Lad-LLM-Proxy.git
   cd Lab-LLM-Proxy
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

Use the provided start script:
```bash
./start_proxy.sh
```

Or run the Python script directly:
```bash
python ollama_proxy.py
```

For custom settings:
```bash
python ollama_proxy.py --host 127.0.0.1 --port 5000
```

For production use, set a strong secret key:
```bash
export SECRET_KEY="your-secure-random-string"
python ollama_proxy.py
```

### Accessing the web interface

Open a browser and navigate to:
```
http://localhost:8080/
```

You will be prompted with a login page. Enter your username and password to access the interface.

<img width="1147" height="868" alt="Screenshot from 2025-10-31 19-11-53" src="https://github.com/user-attachments/assets/4b0a7a87-9719-4595-9583-f28fdf7c660e" />

Simple and clean user interface:

<img width="1147" height="868" alt="Screenshot from 2025-10-31 19-10-36" src="https://github.com/user-attachments/assets/e95da3b2-7494-4744-8e77-845179768cb4" />

### Adding More Models to the LLM Dropdown Menu

Run "ollama list" after installing the Ollama model to see its exact specification:

<img width="733" height="167" alt="Screenshot from 2025-11-01 15-43-51" src="https://github.com/user-attachments/assets/ffa813d6-5b22-41c3-889e-fc8b19909d28" />


update the HTML section of "ollama_proxy.py" and add the new model:

<img width="899" height="242" alt="Screenshot from 2025-10-31 20-18-04" src="https://github.com/user-attachments/assets/3123fee7-c07e-423b-a56e-06448406ac1d" />

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

#### Add More Models 



## Authentication

The server supports two authentication methods:

1. **Web Browser Access**: Form-based login with secure session management
2. **API Access**: HTTP Basic Authentication for programmatic access

Passwords are securely stored using Werkzeug's password hashing functions. The default user accounts are defined in the code, but for production use, you should implement a proper user database.

## Security Enhancements

This implementation includes several security improvements:
- Password hashing using Werkzeug's security functions
- Session-based authentication for web interface
- Random secret key generation (or from environment variable)
- Proper login/logout functionality
- Support for both web and API authentication methods
- Role-based user system (admin/user roles)

## Future Changes 

Create custom LLM training datasets 
Gather more data 
RAG (Retrieval-Augmented Generation) Implementation for reasonalble performance on smaller models (3b parameters)
smaller models used for CPU inference and multiple users. 
## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributors

- [kylanj7](https://github.com/kylanj7)
