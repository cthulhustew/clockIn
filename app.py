from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Set environment configurations
if os.getenv("FLASK_ENV") == "production":
    app.config["ENV"] = "production"
    app.config["DEBUG"] = False
else:
    app.config["ENV"] = "development"
    app.config["DEBUG"] = True

# MongoDB connection function
def get_db_connection():
    client = MongoClient(os.getenv('mongodb+srv://cthulhustew:Klopskerl123%24%24%24@cluster0.mongodb.net/martinaClockIn?retryWrites=true&w=majority'))
    db = client.get_database('martinaClockIn')  # Use your actual database name
    return db

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Assuming you have a templates/index.html file

# Route for clocking in
@app.route('/clock_in', methods=['POST'])
def clock_in():
    db = get_db_connection()
    record = {
        'action': 'Clock In',
        'timestamp': datetime.utcnow()
    }
    db.records.insert_one(record)
    return jsonify({"message": "Clocked In successfully", "status": "success"})

# Route for clocking out
@app.route('/clock_out', methods=['POST'])
def clock_out():
    db = get_db_connection()
    record = {
        'action': 'Clock Out',
        'timestamp': datetime.utcnow()
    }
    db.records.insert_one(record)
    return jsonify({"message": "Clocked Out successfully", "status": "success"})

if __name__ == '__main__':
    app.run()
