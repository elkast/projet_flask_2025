from flask import Blueprint, jsonify, session
from models import rdv_model, patient_model
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/dashboard-data/<int:patient_id>')
def get_dashboard_data(patient_id):
    """Get real-time dashboard data for a patient"""
    try:
        if 'patient_id' not in session or session['patient_id'] != patient_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get patient info
        patient = patient_model.get_patient_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Get all appointments for this patient
        rendez_vous = rdv_model.get_rdv_by_patient_id(patient_id)
        
        # Calculate statistics
        total_rdv = len(rendez_vous)
        rdv_programmes = len([rdv for rdv in rendez_vous if rdv['statut'] == 'Programmé'])
        rdv_termines = len([rdv for rdv in rendez_vous if rdv['statut'] == 'termine'])
        rdv_annules = len([rdv for rdv in rendez_vous if rdv['statut'] == 'annule'])
        
        # Get upcoming appointments (next 3)
        rdv_futurs = [rdv for rdv in rendez_vous if rdv['statut'] == 'Programmé']
        rdv_futurs_sorted = sorted(rdv_futurs, key=lambda x: x['date_heure'])[:3]
        
        # Get recent activity (last 5 appointments)
        rdv_recents = sorted(rendez_vous, key=lambda x: x['date_heure'], reverse=True)[:5]
        
        return jsonify({
            'success': True,
            'patient': {
                'id': patient['id'],
                'nom': patient['nom'],
                'prenom': patient['prenom'],
                'email': patient['email']
            },
            'statistics': {
                'total_rdv': total_rdv,
                'rdv_programmes': rdv_programmes,
                'rdv_termines': rdv_termines,
                'rdv_annules': rdv_annules
            },
            'upcoming_appointments': rdv_futurs_sorted,
            'recent_activity': rdv_recents,
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
