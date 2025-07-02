from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

CLIENTS_FILE = 'clients.csv'
OPPORTUNITIES_FILE = 'opportunities.csv'

# יצירה אוטומטית של קבצים אם לא קיימים
def ensure_file_exists(filename, headers):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

ensure_file_exists(CLIENTS_FILE, [
    'company_name', 'first_name', 'last_name', 'id_number',
    'client_phone', 'contact_phone', 'email', 'sector',
    'source', 'notes', 'created_at', 'submitted_by'
])

ensure_file_exists(OPPORTUNITIES_FILE, [
    'client_name', 'opportunity_name', 'status', 'forecast',
    'notes', 'created_at', 'submitted_by'
])

# שליחת לקוחות
@app.route('/clients', methods=['GET'])
def get_clients():
    with open(CLIENTS_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader))

# שמירת לקוח חדש
@app.route('/clients', methods=['POST'])
def add_client():
    data = request.json
    data['created_at'] = datetime.now().isoformat()
    with open(CLIENTS_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'company_name', 'first_name', 'last_name', 'id_number',
            'client_phone', 'contact_phone', 'email', 'sector',
            'source', 'notes', 'created_at', 'submitted_by'
        ])
        writer.writerow(data)
    return jsonify({'message': 'הלקוח נשמר בהצלחה'})

# שליחת הזדמנויות
@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    with open(OPPORTUNITIES_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return jsonify(list(reader))

# שמירת הזדמנות חדשה
@app.route('/opportunities', methods=['POST'])
def add_opportunity():
    data = request.json
    data['created_at'] = datetime.now().isoformat()
    with open(OPPORTUNITIES_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'client_name', 'opportunity_name', 'status', 'forecast',
            'notes', 'created_at', 'submitted_by'
        ])
        writer.writerow(data)
    return jsonify({'message': 'הזדמנות נשמרה בהצלחה'})

if __name__ == '__main__':
    app.run(debug=True)
