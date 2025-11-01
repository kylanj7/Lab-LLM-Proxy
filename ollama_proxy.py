from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session, flash
from functools import wraps
import requests
import logging
import argparse
import os
import hashlib
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(16)  # Generate random secret key

# User database - in production, use a proper database
USERS = {
    "Kylan": {
        "password_hash": generate_password_hash("password1"),
        "role": "admin"
    },
    "name": {
        "password_hash": generate_password_hash("password2"),
        "role": "user"
    },
    "name": {
        "password_hash": generate_password_hash("password3"),
        "role": "user"
    },
    "name": {
        "password_hash": generate_password_hash("password4"),
        "role": "user"
    },
    "name": {
        "password_hash": generate_password_hash("password5"),
        "role": "user"
    }
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

# API Authentication decorator
def api_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # First check for session-based auth (for browser)
        if 'username' in session:
            return f(*args, **kwargs)
            
        # Then check for Basic auth (for API calls)
        auth = request.authorization
        if auth and auth.username in USERS and check_password_hash(USERS[auth.username]['password_hash'], auth.password):
            return f(*args, **kwargs)
            
        # If we get here, authentication failed
        return jsonify({"error": "Authentication required"}), 401
    return decorated

# Login page template
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ollama Proxy - Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 8px; box-sizing: border-box; }
        button { background: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
        .alert { padding: 10px; background-color: #f44336; color: white; margin-bottom: 15px; }
    </style>
</head>
<body>
    <h1>Ollama Proxy Login</h1>
    
    {% if error %}
    <div class="alert">{{ error }}</div>
    {% endif %}
    
    <form method="post" action="{{ url_for('login') }}">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <button type="submit">Login</button>
    </form>
</body>
</html>
'''

# Home page template
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ollama Home Server</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        textarea { width: 100%; height: 150px; margin-bottom: 10px; padding: 10px; }
        select { width: 100%; padding: 10px; margin-bottom: 10px; }
        button { background: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
        #response { margin-top: 20px; border: 1px solid #ddd; padding: 15px; min-height: 100px; white-space: pre-wrap; }
        .loader { display: none; border: 5px solid #f3f3f3; border-top: 5px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 2s linear infinite; margin: 20px 0; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .user-info { text-align: right; margin-bottom: 20px; }
        .user-info a { color: #666; text-decoration: none; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="user-info">
        Logged in as {{ session.username }} | <a href="{{ url_for('logout') }}">Logout</a>
    </div>

    <h1>Ollama Home Server</h1>
    
    <p>Select model:</p>
    <select id="model">
        <option value="llama3.2:3b">Llama 3.2 (3B)</option>
        <option value="qwen3-vl:32b">Qwen3-VL (32B)</option>
        <option value="gpt-oss:20b">GPT-OSS (20B)</option>
    </select>
    
    <p>Enter your prompt:</p>
    <textarea id="prompt" placeholder="Enter your prompt here..."></textarea>
    
    <div>
        <button onclick="generateText()">Generate</button>
        <div class="loader" id="loader"></div>
    </div>
    
    <div id="response"></div>

    <script>
        function generateText() {
            const prompt = document.getElementById('prompt').value;
            const model = document.getElementById('model').value;
            
            if (!prompt) return;
            
            document.getElementById('loader').style.display = 'block';
            document.getElementById('response').textContent = '';
            
            fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    prompt: prompt,
                    model: model
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Authentication failed or server error');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('response').textContent = data.response;
                document.getElementById('loader').style.display = 'none';
            })
            .catch(error => {
                document.getElementById('response').textContent = 'Error: ' + error.message;
                document.getElementById('loader').style.display = 'none';
            });
        }
    </script>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and check_password_hash(USERS[username]['password_hash'], password):
            session['username'] = username
            session['role'] = USERS[username]['role']
            
            # Redirect to next parameter if available, otherwise to home
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            error = 'Invalid username or password'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/generate', methods=['POST'])
@api_auth_required
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    model = data.get('model', 'llama3.2:3b')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    logger.info(f"Generating response for prompt: {prompt[:50]}... using model {model}")
    
    try:
        # Forward the request to Ollama's API
        ollama_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        ollama_response.raise_for_status()
        response_data = ollama_response.json()
        
        logger.info("Generation complete")
        return jsonify({"response": response_data.get('response', '')})
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/models', methods=['GET'])
@api_auth_required
def list_models():
    try:
        # Get the list of models from Ollama
        ollama_response = requests.get('http://localhost:11434/api/tags')
        ollama_response.raise_for_status()
        
        return jsonify(ollama_response.json())
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Ollama proxy server')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port to run the server on')
    args = parser.parse_args()
    
    logger.info(f"Starting Ollama proxy server on {args.host}:{args.port}")
    
    # Run the Flask app
    app.run(host=args.host, port=args.port, debug=False)
