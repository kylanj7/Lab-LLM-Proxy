from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
from functools import wraps
import requests
import logging
import argparse
import os
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
# Generate a secure random secret key for sessions
app.secret_key = secrets.token_hex(16)

# User authentication - in production, use a more secure method
USERS = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
    "user5": "password5",
}

# Login required decorator
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get auth from request header OR from URL parameters
        auth = request.authorization
        
        # Check URL parameters if header auth is not present
        if not auth:
            username = request.args.get('username')
            password = request.args.get('password')
            
            if username in USERS and USERS[username] == password:
                return f(*args, **kwargs)
        
        # Check header auth
        elif auth.username in USERS and USERS[auth.username] == auth.password:
            return f(*args, **kwargs)
        
        # If we get here, authentication failed
        return jsonify({"error": "Authentication required"}), 401
    return decorated

# Login page template
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ollama Home Server - Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .login-container { max-width: 400px; margin: 100px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 3px; }
        button { background: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; width: 100%; }
        .error { color: red; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login to Ollama Home Server</h2>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <form method="post">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
'''

# Main app template
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
        .header { display: flex; justify-content: space-between; align-items: center; }
        .logout { background: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Ollama Home Server</h1>
        <a href="/logout"><button class="logout">Logout</button></a>
    </div>
    
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
                    if (response.status === 401) {
                        window.location.href = '/login';
                        throw new Error('Session expired. Please log in again.');
                    }
                    throw new Error('Server error');
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
        
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            error = 'Invalid credentials'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/generate', methods=['POST'])
@login_required
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
@login_required
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
    parser.add_argument('--port', type=int, default=8000,
                        help='Port to run the server on')
    args = parser.parse_args()
    
    logger.info(f"Starting Ollama proxy server on {args.host}:{args.port}")
    
    # Run the Flask app
    app.run(host=args.host, port=args.port, debug=False)
