from flask import Blueprint, render_template, jsonify, request
from datetime import datetime
from models.medecin_model import get_medecins as lister_medecins, get_medecin_by_id as trouver_medecin_par_id, Medecin
from models.rdv_model import RendezVous
from models import db

medecin_bp = Blueprint('medecin', __name__, url_prefix='/medecins')

@medecin_bp.route('/')
def liste_medecins():
    """Afficher la liste de tous les médecins"""
    try:
        medecins = lister_medecins()
        return render_template('medecins/liste.html', medecins=medecins)
    except Exception as e:
        return render_template('medecins/liste.html', medecins=[], error=str(e))

@medecin_bp.route('/api/liste')
def api_liste_medecins():
    """API endpoint pour récupérer la liste des médecins en JSON"""
    try:
        medecins = lister_medecins()
        response = jsonify({
            'success': True,
            'medecins': medecins,
            'total': len(medecins)
        })
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        response = jsonify({
            'success': False,
            'error': str(e)
        })
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response, 500

@medecin_bp.route('/api/statistiques')
def api_statistiques():
    """API endpoint pour les statistiques en temps réel"""
    try:
        # Nombre total de médecins
        total_medecins = Medecin.query.count()

        # Maintenant
        maintenant = datetime.now()

        # Médecins avec des RDV à venir
        medecins_disponibles = db.session.query(db.func.count(db.distinct(RendezVous.medecin_id)))\
            .filter(RendezVous.date_heure >= maintenant).scalar() or 0

        # Total RDV
        total_rdv = RendezVous.query.count()

        # RDV programmés (futurs)
        rdv_programmes = RendezVous.query.filter(RendezVous.date_heure >= maintenant).count()

        response = jsonify({
            'success': True,
            'statistiques': {
                'total_medecins': total_medecins,
                'medecins_disponibles': medecins_disponibles,
                'total_rdv': total_rdv,
                'rdv_programmes': rdv_programmes
            }
        })
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        response = jsonify({
            'success': False,
            'error': str(e)
        })
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response, 500

@medecin_bp.route('/<int:medecin_id>')
def details_medecin(medecin_id):
    """Afficher les détails d'un médecin spécifique"""
    try:
        medecin = trouver_medecin_par_id(medecin_id)
        if not medecin:
            return render_template('404.html'), 404

        # Récupérer les prochains rendez-vous (à partir de maintenant) en ORM
        maintenant = datetime.now()
        rdvs = db.session.query(RendezVous, Patient).join(Patient, RendezVous.patient_id == Patient.id)\
            .filter(RendezVous.medecin_id == medecin_id, RendezVous.date_heure >= maintenant)\
            .order_by(RendezVous.date_heure).all()

        # Adapter les données au template existant
        prochains_rdv = [
            {
                'date_rdv': rdv.date_heure.date(),
                'heure_rdv': rdv.date_heure.strftime('%H:%M'),
                'patient': {
                    'nom': patient.nom,
                    'prenom': patient.prenom
                },
                'motif': rdv.motif
            }
            for rdv, patient in rdvs
        ]

        return render_template('medecins/details.html', 
                             medecin=medecin, 
                             prochains_rdv=prochains_rdv)
    except Exception as e:
        return render_template('medecins/details.html', 
                             medecin=None, 
                             error=str(e))
