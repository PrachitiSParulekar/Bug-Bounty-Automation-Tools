from flask import Flask, json, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import whois
import requests
import re
import sqlite3
from datetime import datetime
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Helper functions
def is_valid_domain(domain):
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def is_valid_ip(ip):
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(ip_pattern, ip))

def init_db():
    conn = sqlite3.connect("recon/recon.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subdomains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            org_name TEXT,
            domain TEXT,
            subdomain TEXT,
            discovered_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_subdomain(org_name, domain, subdomain):
    conn = sqlite3.connect("recon/recon.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO subdomains (org_name, domain, subdomain, discovered_at)
        VALUES (?, ?, ?, ?)
    ''', (org_name, domain, subdomain, datetime.now()))
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/ip_lookup')
def ip_lookup():
    return render_template('ip_lookup.html')

@app.route('/whois')
def whois_lookup():
    return render_template('whois.html')

@app.route('/certificate_search')
def certificate_search():
    return render_template('certificate_search.html')

@app.route('/open_ports')
def open_ports():
    return render_template('open_ports.html')

@app.route('/subfinder')
def subfinder():
    return render_template('subfinder.html')

@app.errorhandler(500)
def handle_500(e):
    app.logger.error(f'Server error: {e}')
    return jsonify({"error": "Internal server error"}), 500

# Socket events
@socketio.on('start_ping')
def start_ping(data):
    try:
        domain = data.get('domain')
        if not domain or not is_valid_domain(domain):
            emit('ping_update', {'error': 'Invalid domain format'})
            return

        with subprocess.Popen(['ping', '-n', '4', domain], 
                            stdout=subprocess.PIPE, 
                            bufsize=1, 
                            universal_newlines=True) as p:
            for line in p.stdout:
                emit('ping_update', {'data': line.strip()})
    except subprocess.SubprocessError as e:
        emit('ping_update', {'error': f'Ping command failed: {str(e)}'})
    except Exception as e:
        emit('ping_update', {'error': f'Unexpected error: {str(e)}'})

@socketio.on('start_iplookup')
def start_iplookup(data):
    try:
        ip_address = data.get('ipAddress')
        if not ip_address or not is_valid_ip(ip_address):
            emit('iplookup_update', {'error': 'Invalid IP address format'})
            return

        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10)
        response.raise_for_status()
        emit('iplookup_update', {'data': response.text})
    except requests.RequestException as e:
        emit('iplookup_update', {'error': f'Network error: {str(e)}'})
    except Exception as e:
        emit('iplookup_update', {'error': f'Unexpected error: {str(e)}'})

@socketio.on('start_whois')
def start_whois(data):
    try:
        domain = data.get('domain')
        if not domain or not is_valid_domain(domain):
            emit('whois_update', {'error': 'Invalid domain'})
            return

        domain_info = whois.whois(domain)
        emit('whois_update', {'data': json.dumps(domain_info)})
    except Exception as e:
        emit('whois_update', {'error': str(e)})

@socketio.on('start_crtsh')
def start_crtsh(data):
    try:
        domain = data.get('domain')
        if not domain or not is_valid_domain(domain):
            emit('crtsh_update', {'error': 'Invalid domain'})
            return

        response = requests.get(f'https://crt.sh/?q=%.{domain}&output=json', timeout=10)
        emit('crtsh_update', {'data': response.text})
    except Exception as e:
        emit('crtsh_update', {'error': str(e)})

@socketio.on('start_openports')
def start_openports(data):
    try:
        domain = data.get('domain')
        if not domain or not is_valid_domain(domain):
            emit('openports_update', {'error': 'Invalid domain'})
            return

        result = subprocess.run(['nmap', '-F', domain], 
                              stdout=subprocess.PIPE, 
                              text=True,
                              timeout=300)
        emit('openports_update', {'data': result.stdout})
    except Exception as e:
        emit('openports_update', {'error': str(e)})

@socketio.on('start_subfinder')
def start_subfinder(data):
    try:
        domain = data.get('domain')
        if not domain or not is_valid_domain(domain):
            emit('subfinder_update', {'error': 'Invalid domain'})
            return
            
        with subprocess.Popen(['subfinder', '-d', domain, '-silent'],
                            stdout=subprocess.PIPE,
                            bufsize=1,
                            universal_newlines=True) as p:
            for line in p.stdout:
                subdomain = line.strip()
                if subdomain:
                    save_subdomain("", domain, subdomain)
                    emit('subfinder_update', {'subdomain': subdomain})
    except Exception as e:
        emit('subfinder_update', {'error': str(e)})

if __name__ == '__main__':
    init_db()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    port = int(os.environ.get('PORT', 5000))
    socketio.run(
        app, 
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
        log_output=True
    )
