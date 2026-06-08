# path: /workspaces/Health_Prediction_App/models/patient.py

from firebase_admin import firestore
#Firestore is a NoSQL cloud database - data stored as documents inside collection

COLLECTION = 'patients'


def create_patient(uid, data):
    db = firestore.client()        # ← get client here, not at module level
    record = {
        'uid':         uid, #for data isolation
        'full_name':   data['full_name'].strip(),
        'dob':         data['dob'],
        'email':       data['email'].strip(),
        'glucose':     float(data['glucose']),
        'haemoglobin': float(data['haemoglobin']),
        'cholesterol': float(data['cholesterol']),
        'remarks':     data.get('remarks', ''),
        'created_at':  firestore.SERVER_TIMESTAMP
    }
    db.collection(COLLECTION).add(record)


def read_patients(uid):
    db = firestore.client()        # ← get client here
    docs = (
        db.collection(COLLECTION)
          .where('uid', '==', uid)
          .stream()
    )
    patients = []
    for doc in docs:
        p = doc.to_dict()
        p['id'] = doc.id
        p.pop('created_at', None)
        patients.append(p)
    return patients


def update_patient(doc_id, uid, data):
    db = firestore.client()        # ← get client here
    doc_ref = db.collection(COLLECTION).document(doc_id)
    doc     = doc_ref.get()

    #checks if document id doesnt exist at all or it exists in different database
    if not doc.exists or doc.to_dict().get('uid') != uid:
        return False

    doc_ref.update({
        'full_name':   data['full_name'].strip(),
        'dob':         data['dob'],
        'email':       data['email'].strip(),
        'glucose':     float(data['glucose']),
        'haemoglobin': float(data['haemoglobin']),
        'cholesterol': float(data['cholesterol']),
        'remarks':     data.get('remarks', '')
    })
    return True


def delete_patient(doc_id, uid):
    db = firestore.client()        # get client here
    doc_ref = db.collection(COLLECTION).document(doc_id)
    doc = doc_ref.get()

    if not doc.exists or doc.to_dict().get('uid') != uid:
        return False

    doc_ref.delete()
    return True