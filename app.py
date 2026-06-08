# path: D:\Projects\Health_Prediction_App\app.py

import os      #read environment variables and file paths
import sys     #modify Python module search path.
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
# Flask - entire app, 
# request — reads incoming HTTP data
# render_template — renders HTML files from templates folder
# redirect / url_for — sends user to another route
# flash — one-time messages shown to the user 
# session — stores data across requests (like who is logged in)
# jsonify — converts Python dicts to JSON responses
import firebase_admin
from firebase_admin import credentials, auth
#create user, verify authentication server side
import requests as http_requests #making HTTP calls
from dotenv import load_dotenv #read .env file into environment variables
from datetime import datetime #date validation

sys.path.insert(0, os.path.dirname(__file__))

from models.patient import create_patient, read_patients, update_patient, delete_patient
from services.ai_service import generate_health_remarks

load_dotenv()
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
# gives server admin level access to Firebase 

# ──User────────────────────────────────────────────────────────────────────

def logged_in():  #if user has a user_id stored in their session
    return 'user_id' in session

def validate_patient(data):    # Validates patient data form data before saving to the database.
    if not data.get('full_name', '').strip():
        return "Full name is required."
    try:
        dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        if dob >= datetime.today().date():
            return "Date of birth cannot be today or a future date."
    except (ValueError, KeyError):
        return "Invalid date of birth."
    email = data.get('email', '')
    if '@' not in email or '.' not in email:
        return "Invalid email address."
    for field in ['glucose', 'haemoglobin', 'cholesterol']:
        try:
            if float(data[field]) <= 0:
                raise ValueError
        except (ValueError, KeyError, TypeError):
            return f"{field.capitalize()} must be a positive number."
    return None


# ── Auth Routes ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard') if logged_in() else url_for('login'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        try:
            auth.create_user(email=email, password=password)
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Signup Error: {str(e)}", "danger")
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login(): #Uses Firebase's REST API
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        url      = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        response = http_requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        data     = response.json()
        if response.status_code == 200:
            session['user_id'] = data['localId']   # uid for data isolation
            session['email']   = data['email']
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash(f"Login Failed: {data.get('error',{}).get('message','Invalid credentials')}", "danger")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


# ── Page Routes─────────────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        flash("Please login first!", "warning")
        return redirect(url_for('login'))
    return render_template("dashboard.html", email=session['email'])

@app.route('/add_patient')
def add_patient_page():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template("add_patient.html", email=session['email'])


# ── Patient APIRoutes  ───────────────────────────────────────────────────────────────

@app.route('/api/patients', methods=['GET'])
def api_read_patients():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'patients': read_patients(session['user_id'])})

@app.route('/api/patients', methods=['POST'])
#receives JSON data, validates it, then saves the patient linked to the current user's ID.
def api_create_patient():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data   = request.get_json()
    errors = validate_patient(data)
    if errors:
        return jsonify({'error': errors}), 400
    create_patient(session['user_id'], data)                   
    return jsonify({'success': True})

@app.route('/api/patients/<doc_id>', methods=['PUT'])
def api_update_patient(doc_id):
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data   = request.get_json()
    errors = validate_patient(data)
    if errors:
        return jsonify({'error': errors}), 400
    if not update_patient(doc_id, session['user_id'], data):
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify({'success': True})

@app.route('/api/patients/<doc_id>', methods=['DELETE'])
def api_delete_patient(doc_id):
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    if not delete_patient(doc_id, session['user_id']): 
        return jsonify({'error': 'Forbidden'}), 403
    return jsonify({'success': True})


# ── AI Remarks Route ────────────────────────────────────────────────────────────────

@app.route('/generate_remarks', methods=['POST'])
def api_generate_remarks():
    if not logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    try:
        remarks = generate_health_remarks(
            data.get('glucose'),
            data.get('haemoglobin'),
            data.get('cholesterol')
        )
        return jsonify({'remarks': remarks})
    except Exception as e:
        return jsonify({'error': f'AI generation failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)