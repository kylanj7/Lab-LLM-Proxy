# Lab-vLLM-Server

Fast Local inference for 5+ users (under 15 secounds) using the llama3.2:3b model. Server SPECS: 3090ti, Epyc 7302 & 128GB DDR4 @ 2666MT/s 1Gb small home network

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
   git clone https://github.com/kylanj7/Local-vLLM-with-Ollama-Models.git
   cd Local-vLLM-with-Ollama-Models
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
Simple and clean user interface:

<img width="1147" height="868" alt="Screenshot from 2025-10-31 19-10-36" src="https://github.com/user-attachments/assets/e95da3b2-7494-4744-8e77-845179768cb4" />

You will be prompted with a login page. Enter your username and password to access the interface.

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

## Future Improvements

For production deployment, consider:
- Moving user data to a proper database
- Implementing user registration and management
- Adding HTTPS support
- Implementing password reset functionality
- Adding rate limiting for API calls
- Implementing CSRF protection

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributors

- [kylanj7](https://github.com/kylanj7)
