from flask import Flask, request, jsonify, redirect, abort
from datetime import datetime
import random
import string
import threading

app = Flask(__name__)

lock = threading.Lock()
url_store = {}  
@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    original_url = data['url']
    if not original_url.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid URL format'}), 400

    with lock:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        while code in url_store:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        url_store[code] = {
            'url': original_url,
            'created_at': datetime.utcnow(),
            'clicks': 0
        }

    short_url = request.host_url + code
    return jsonify({'short_code': code, 'short_url': short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    with lock:
        data = url_store.get(short_code)
        if not data:
            return abort(404, description="Short code not found")
        data['clicks'] += 1
        return redirect(data['url'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    with lock:
        data = url_store.get(short_code)
        if not data:
            return jsonify({'error': 'Short code not found'}), 404

        return jsonify({
            'url': data['url'],
            'clicks': data['clicks'],
            'created_at': data['created_at'].isoformat() + 'Z'
        })
