from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Set environment configurations
if os.getenv("FLASK_ENV") == "production":
    app.config["ENV"] = "production"
    app.config["DEBUG"] = False
else:
    app.config["ENV"] = "development"
    app.config["DEBUG"] = True

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('time_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Assuming you have a templates/index.html file

# Route for clocking in
@app.route('/clock_in', methods=['POST'])
def clock_in():
    conn = sqlite3.connect('time_records.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO records (action) VALUES (?)', ('Clock In',))
    conn.commit()
    conn.close()
    return jsonify({"message": "Clocked In successfully", "status": "success"})

# Route for clocking out
@app.route('/clock_out', methods=['POST'])
def clock_out():
    conn = sqlite3.connect('time_records.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO records (action) VALUES (?)', ('Clock Out',))
    conn.commit()
    conn.close()
    return jsonify({"message": "Clocked Out successfully", "status": "success"})

if __name__ == '__main__':
    init_db()
    app.run()
