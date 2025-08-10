from models import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)
    
    def __repr__(self):
        return f'<Patient {self.prenom} {self.nom}>'

# Helper functions for patient operations
def get_patient_by_email(email):
    """Get a patient by email address."""
    patient = Patient.query.filter_by(email=email).first()
    if patient:
        return {
            'id': patient.id,
            'nom': patient.nom,
            'prenom': patient.prenom,
            'email': patient.email,
            'mot_de_passe': patient.mot_de_passe,
            'date_naissance': patient.date_naissance,
            'telephone': patient.telephone,
            'created_at': patient.created_at,
            'updated_at': patient.updated_at
        }
    return None

def get_patient_by_id(patient_id):
    """Get a patient by ID."""
    patient = Patient.query.get(patient_id)
    if patient:
        return {
            'id': patient.id,
            'nom': patient.nom,
            'prenom': patient.prenom,
            'email': patient.email,
            'mot_de_passe': patient.mot_de_passe,
            'date_naissance': patient.date_naissance,
            'telephone': patient.telephone,
            'created_at': patient.created_at,
            'updated_at': patient.updated_at
        }
    return None

def create_patient(nom, prenom, email, mot_de_passe, date_naissance, telephone=None):
    """Create a new patient."""
    try:
        new_patient = Patient(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=mot_de_passe,
            date_naissance=date_naissance,
            telephone=telephone
        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient.id
    except Exception as e:
        db.session.rollback()
        return None

def update_patient(patient_id, nom, prenom, email, date_naissance, telephone=None):
    """Update an existing patient's information."""
    try:
        patient = Patient.query.get(patient_id)
        if patient:
            patient.nom = nom
            patient.prenom = prenom
            patient.email = email
            patient.date_naissance = date_naissance
            patient.telephone = telephone
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        return False
