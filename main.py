from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

CLIENTS_FILE = 'clients.csv'
OPPORTUNITIES_FILE = 'opportunities.csv'

def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(data.keys())
        writer.writerow(data.values())

def load_from_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

@app.route('/')
def index():
    return jsonify({"message": "ProMiXed CRM API is running 🎉"})

@app.route('/clients', methods=['POST', 'GET'])
def clients():
    if request.method == 'POST':
        data = request.get_json()
        data['timestamp'] = datetime.utcnow().isoformat()
        save_to_csv(data, CLIENTS_FILE)
        return jsonify({'message': 'Client saved successfully'}), 200
    else:
        data = load_from_csv(CLIENTS_FILE)
        return jsonify(data)

@app.route('/opportunities', methods=['POST', 'GET'])
def opportunities():
    if request.method == 'POST':
        data = request.get_json()
        data['timestamp'] = datetime.utcnow().isoformat()
        save_to_csv(data, OPPORTUNITIES_FILE)
        return jsonify({'message': 'Opportunity saved successfully'}), 200
    else:
        data = load_from_csv(OPPORTUNITIES_FILE)
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
