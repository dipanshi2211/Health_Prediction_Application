# Health Prediction Application

A Flask Web application that stores patient blood test records in Firebase and uses Groq API to generate short summary of health risk reports.

---

## Tech Stack :
| Layer           |      Technology                      |
|-----------------|--------------------------------------|
| Frontend        | HTML, Bootstrap 5, Vanilla JS.       |
| Backend         |Python, Flask                         |
| Database / Auth | Firebase (Firestore + Firebase Auth) |
| AI — Groq API   | (llama-3.1-8b-instant)               |

---

## Features :
- Signup / Login via Firebase Authentication
- **CRUD** Create, Read, Update, Delete patient records
- Blood test inputs : Glucose, Haemoglobin, Cholesterol
- AI-generated health remarks via Groq (2-sentence summary, no diagnosis)
- Server-side validation — email format, future DOB check, positive numeric fields
- Per-user data isolation (each user only sees their own records)

---

## App collects and manages following information for each patient:
• Full Name
• Date of Birth (can not be future date)
• Email Address (should be valid)
• Glucose (numeric)
• Haemoglobin (numeric)
• Cholesterol (numeric)
• Remarks (Generated from Groq AI)

---

## Project Structure

```
Health_Prediction_App/
├── app.py                      # Main Flask application file  
├── requirements.txt
├── .env
├── .gitignore
├── serviceAccountKey.json      # excluded from git
├── models/
│   ├── __init__.py
│   └── patient.py              # Firebase CRUD functonality
├── services/
│   ├── __init__.py
│   └── ai_service.py           # Groq API call
└── templates/                  # Flask automatically looks here for HTML files - used to send POST data
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    └── add_patient.html
```

---

## Setup

**1. Git Clone the repo**
```bash
git clone https://github.com/<your-username>/Health_Prediction_App.git
cd Health_Prediction_App
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your `.env` file**
```
FLASK_SECRET_KEY=your_secret_key
FIREBASE_WEB_API_KEY=your_firebase_web_api_key
GROQ_API_KEY=your_groq_api_key
```

**4. Add your Firebase service account**
Download `serviceAccountKey.json` from Firebase Console → Project Settings → Service Accounts and place it in the root folder. It's already excluded from git.

**5. Run**
```bash
python app.py
```

**6. View**
Open `http://127.0.0.1:5000` in your browser.

---

## Environment Variables

|    Variable            |                Description               |
|------------------------|------------------------------------------|
| `FLASK_SECRET_KEY`    | Flask session secret                     |
| `FIREBASE_WEB_API_KEY` | From Firebase Console → Project Settings |
| `GROQ_API_KEY`         | From console.groq.com                    |

--- 

## Blood Test Reference Ranges

| Marker      | Low      | Normal             | Borderline / High     |
|-------------|----------|--------------------|-----------------------|
| Glucose     | <70 mg/dL | 70–99 mg/dL        | 100–125 / >125 mg/dL  |
| Haemoglobin | <12 g/dL  | 12–17.5 g/dL       | >17.5 g/dL            |
| Cholesterol | —         | <200 mg/dL         | 200–239 / ≥240 mg/dL  |

--- 

## Notes

- `serviceAccountKey.json` and `.env` are in `.gitignore` — never commit them
- Remarks are optional; a patient record can be saved without generating them
- The AI summary is informational only and does not constitute medical advice

## Video Explanation of this Project
https://drive.google.com/file/d/18PTeL2_YFCC4alqcnX66xJfOdeOV925-/view?usp=drive_link
