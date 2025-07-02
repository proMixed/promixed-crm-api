from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)

CLIENTS_FILE = 'clients.csv'
OPPORTUNITIES_FILE = 'opportunities.csv'

def save_to_csv(data, filename):
    data['timestamp'] = datetime.now().isoformat()
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@app.route('/clients', methods=['POST'])
def save_client():
    data = request.get_json()
    save_to_csv(data, CLIENTS_FILE)
    return jsonify({'message': 'הלקוח נשמר בהצלחה'})

@app.route('/clients', methods=['GET'])
def get_clients():
    try:
        with open(CLIENTS_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
        return jsonify(rows)
    except FileNotFoundError:
        return jsonify([])

@app.route('/opportunities', methods=['POST'])
def save_opportunity():
    data = request.get_json()
    save_to_csv(data, OPPORTUNITIES_FILE)
    return jsonify({'message': 'ההזדמנות נשמרה בהצלחה'})

@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    try:
        with open(OPPORTUNITIES_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
        return jsonify(rows)
    except FileNotFoundError:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
