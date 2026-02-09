import uuid
import logging
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from collections import deque

app = Flask(__name__)

# Store access logs
access_logs = deque(maxlen=1000)  # Store up to 1000 logs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Home route: Assign UUID to client and render page"""
    client_uuid = str(uuid.uuid4())
    logger.info(f"Assigned UUID to client: {client_uuid}")
    return render_template('index.html', uuid=client_uuid)


@app.route('/page')
def page():
    """Home route: Assign UUID to client and render page"""
    client_uuid = str(uuid.uuid4())
    logger.info(f"Assigned UUID to client: {client_uuid}")
    return render_template('index.html', uuid=client_uuid)

@app.route('/test')
def test():
    """Test route: Assign UUID to client and render page"""
    client_uuid = str(uuid.uuid4())
    logger.info(f"Assigned UUID to client: {client_uuid}")
    return render_template('test.html', uuid=client_uuid)

@app.route('/auth')
def auth():
    """Auth route: Record access logs"""
    client_uuid = request.args.get('uuid', 'unknown')
    data = request.args.get('data', '')
    
    # Get client information
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'unknown')
    timestamp = datetime.now().isoformat()
    
    # Record log
    log_entry = {
        'timestamp': timestamp,
        'ip': client_ip,
        'user_agent': user_agent,
        'uuid': client_uuid,
        'data': data
    }
    
    access_logs.append(log_entry)
    
    logger.info(f"Auth access - IP: {client_ip}, UUID: {client_uuid}, Data: {data}")
    
    return jsonify({
        'status': 'success',
        'message': 'Log recorded',
        'uuid': client_uuid,
        'data': data
    })


@app.route('/logs')
def logs():
    """Logs route: Display all auth access logs"""
    return render_template('logs.html', logs=list(access_logs))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404


if __name__ == '__main__':
    logger.info("Starting web server...")
    
    # SSL certificate configuration
    cert_file = os.environ.get('SSL_CERT_FILE', 'cert.pem')
    key_file = os.environ.get('SSL_KEY_FILE', 'key.pem')
    
    # Check if SSL certificates exist
    ssl_context = None
    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_context = (cert_file, key_file)
        logger.info(f"Using SSL certificates: {cert_file}, {key_file}")
        app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=ssl_context)
    else:
        logger.warning("SSL certificates not found, running in HTTP mode")
        logger.info(f"To enable HTTPS, place certificate files at:")
        logger.info(f"  Certificate: {cert_file}")
        logger.info(f"  Key: {key_file}")
        logger.info(f"Or set environment variables: SSL_CERT_FILE and SSL_KEY_FILE")
        app.run(debug=True, host='0.0.0.0', port=5000)
