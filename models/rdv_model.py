from models import db
from datetime import datetime

class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecins.id'), nullable=False)
    date_heure = db.Column(db.DateTime, nullable=False)
    duree = db.Column(db.Integer, default=30)  # durée en minutes
    motif = db.Column(db.String(500), nullable=True)
    statut = db.Column(db.String(20), default='planifie')  # planifie, confirme, annule, termine
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RendezVous {self.date_heure} - Patient {self.patient_id} - Dr {self.medecin_id}>'

# Helper functions for rendez-vous operations
def get_rdv_by_patient_id(patient_id):
    """Get all rendez-vous for a specific patient with medecin details."""
    from models.medecin_model import Medecin
    
    rendez_vous = RendezVous.query.filter_by(patient_id=patient_id).all()
    result = []
    
    for rdv in rendez_vous:
        medecin = Medecin.query.get(rdv.medecin_id)
        if medecin:
            result.append({
                'id': rdv.id,
                'patient_id': rdv.patient_id,
                'medecin_id': rdv.medecin_id,
                'medecin_nom': medecin.nom,
                'medecin_prenom': medecin.prenom,
                'specialite': medecin.specialite,
                'date_heure': rdv.date_heure,
                'duree': rdv.duree,
                'motif': rdv.motif,
                'statut': rdv.statut,
                'notes': rdv.notes,
                'date_creation': rdv.created_at,
                'updated_at': rdv.updated_at
            })
    
    return result

def create_rdv(date_heure, motif, patient_id, medecin_id, duree=30):
    """Create a new rendez-vous."""
    try:
        new_rdv = RendezVous(
            date_heure=date_heure,
            motif=motif,
            patient_id=patient_id,
            medecin_id=medecin_id,
            duree=duree
        )
        db.session.add(new_rdv)
        db.session.commit()
        return new_rdv.id
    except Exception as e:
        db.session.rollback()
        return None

def get_rdv_by_id(rdv_id):
    """Get a rendez-vous by ID."""
    rdv = RendezVous.query.get(rdv_id)
    if rdv:
        return {
            'id': rdv.id,
            'patient_id': rdv.patient_id,
            'medecin_id': rdv.medecin_id,
            'date_heure': rdv.date_heure,
            'duree': rdv.duree,
            'motif': rdv.motif,
            'statut': rdv.statut,
            'notes': rdv.notes,
            'created_at': rdv.created_at,
            'updated_at': rdv.updated_at
        }
    return None

def cancel_rdv(rdv_id):
    """Cancel a rendez-vous."""
    try:
        rdv = RendezVous.query.get(rdv_id)
        if rdv:
            rdv.statut = 'annule'
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        return False
