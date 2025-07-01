from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

CLIENTS_FILE = 'clients.json'
OPPORTUNITIES_FILE = 'opportunities.json'

def save_to_file(file_path, data):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)

    with open(file_path, 'r+', encoding='utf-8') as f:
        items = json.load(f)
        items.append(data)
        f.seek(0)
        json.dump(items, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return {'message': 'ProMiXed CRM API is running 🎉'}

@app.route('/clients', methods=['GET'])
def get_clients():
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, 'r', encoding='utf-8') as f:
            clients = json.load(f)
    else:
        clients = []
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    data['timestamp'] = datetime.now().isoformat()
    save_to_file(CLIENTS_FILE, data)
    return {'message': 'הלקוח נשמר בהצלחה'}

@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    if os.path.exists(OPPORTUNITIES_FILE):
        with open(OPPORTUNITIES_FILE, 'r', encoding='utf-8') as f:
            opportunities = json.load(f)
    else:
        opportunities = []
    return jsonify(opportunities)

@app.route('/opportunities', methods=['POST'])
def add_opportunity():
    data = request.get_json()
    data['timestamp'] = datetime.now().isoformat()
    save_to_file(OPPORTUNITIES_FILE, data)
    return {'message': 'ההזדמנות נשמרה בהצלחה'}

if __name__ == '__main__':
    app.run(debug=True)
