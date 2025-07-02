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
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def read_from_csv(filename):
    if not os.path.isfile(filename):
        return []
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        data = request.get_json()
        data['timestamp'] = datetime.now().isoformat()
        save_to_csv(data, CLIENTS_FILE)
        return jsonify({'message': 'הלקוח נשמר בהצלחה'})
    else:
        return jsonify(read_from_csv(CLIENTS_FILE))


@app.route('/opportunities', methods=['GET', 'POST'])
def opportunities():
    if request.method == 'POST':
        data = request.get_json()
        data['timestamp'] = datetime.now().isoformat()
        save_to_csv(data, OPPORTUNITIES_FILE)
        return jsonify({'message': 'ההזדמנות נשמרה בהצלחה'})
    else:
        return jsonify(read_from_csv(OPPORTUNITIES_FILE))


if __name__ == '__main__':
    app.run(debug=True)
