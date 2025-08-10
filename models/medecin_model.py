from models import db
from datetime import datetime

class Medecin(db.Model):
    __tablename__ = 'medecins'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    adresse = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    rendez_vous = db.relationship('RendezVous', backref='medecin', lazy=True)
    
    def __repr__(self):
        return f'<Medecin Dr. {self.prenom} {self.nom}>'

# Helper functions for medecin operations
def create_medecin(nom, prenom, email, mot_de_passe, specialite, telephone=None, adresse=None):
    """Create a new medecin."""
    try:
        new_medecin = Medecin(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=mot_de_passe,
            specialite=specialite,
            telephone=telephone,
            adresse=adresse
        )
        db.session.add(new_medecin)
        db.session.commit()
        return new_medecin.id
    except Exception as e:
        db.session.rollback()
        return None

def get_medecin_by_id(medecin_id):
    """Get a medecin by ID."""
    medecin = Medecin.query.get(medecin_id)
    if medecin:
        return {
            'id': medecin.id,
            'nom': medecin.nom,
            'prenom': medecin.prenom,
            'email': medecin.email,
            'specialite': medecin.specialite,
            'telephone': medecin.telephone,
            'adresse': medecin.adresse,
            'created_at': medecin.created_at,
            'updated_at': medecin.updated_at
        }
    return None

def get_medecins():
    """Get all medecins."""
    medecins = Medecin.query.all()
    return [
        {
            'id': m.id,
            'nom': m.nom,
            'prenom': m.prenom,
            'email': m.email,
            'specialite': m.specialite,
            'telephone': m.telephone,
            'adresse': m.adresse,
            'created_at': m.created_at,
            'updated_at': m.updated_at
        }
        for m in medecins
    ]
