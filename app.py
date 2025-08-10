from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from models import db
from models.patient_model import Patient
from models.medecin_model import Medecin
from models.rdv_model import RendezVous
from controllers.patient_controller import patient_inscription, patient_connexion, patient_dashboard, patient_profil, patient_deconnexion
from controllers.medecin_controller import medecin_bp
from controllers.api_controller import api_bp
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

# Configuration simple
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Initialisation
db.init_app(app)

# Créer les tables
with app.app_context():
    db.create_all()

# Blueprints
app.register_blueprint(medecin_bp)
app.register_blueprint(api_bp)

# Routes principales simplifiées
@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Vérification santé"""
    return jsonify({
        'statut': 'opérationnel',
        'base_de_donnees': 'connectée'
    })

# Routes API simplifiées
@app.route('/api/patients')
def api_patients():
    """Liste des patients"""
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'email': p.email,
        'telephone': p.telephone
    } for p in patients])

@app.route('/api/medecins')
def api_medecins():
    """Liste des médecins"""
    medecins = Medecin.query.all()
    return jsonify([{
        'id': m.id,
        'nom': m.nom,
        'specialite': m.specialite
    } for m in medecins])

@app.route('/api/rdv')
def api_rdv():
    """Liste des rendez-vous"""
    rdvs = RendezVous.query.all()
    return jsonify([{
        'id': r.id,
        'date': r.date_heure.isoformat() if r.date_heure else None,
        'motif': r.motif
    } for r in rdvs])

# Routes patients simplifiées
@app.route('/patient/connexion', methods=['GET', 'POST'])
def patient_connexion():
    """Connexion patient"""
    from controllers.patient_controller import patient_connexion as connexion_func
    return connexion_func()

@app.route('/patient/inscription', methods=['GET', 'POST'])
def patient_inscription():
    """Inscription patient"""
    from controllers.patient_controller import patient_inscription as inscription_func
    return inscription_func()

@app.route('/patient/dashboard')
def patient_dashboard():
    """Dashboard patient"""
    from controllers.patient_controller import patient_dashboard as dashboard_func
    return dashboard_func()

@app.route('/patient/profil', methods=['GET', 'POST'])
def patient_profil():
    """Profil patient"""
    from controllers.patient_controller import patient_profil as profil_func
    return profil_func()

@app.route('/patient/deconnexion')
def patient_deconnexion():
    """Déconnexion patient"""
    from controllers.patient_controller import patient_deconnexion as deconnexion_func
    return deconnexion_func()

@app.route('/rdv/nouveau', methods=['GET', 'POST'])
def nouveau_rdv():
    """Créer un nouveau rendez-vous"""
    from controllers.rdv_controller import nouveau_rdv as nouveau_rdv_ctrl
    return nouveau_rdv_ctrl()

@app.route('/rdv/liste')
def liste_rdv():
    """Liste des rendez-vous"""
    from controllers.rdv_controller import liste_rdv as liste_rdv_func
    return liste_rdv_func()

@app.route('/rdv/details/<int:rdv_id>')
def rdv_details(rdv_id):
    """Détails d'un rendez-vous"""
    from controllers.rdv_controller import details_rdv as details_rdv_func
    return details_rdv_func(rdv_id)

@app.route('/rdv/annuler/<int:rdv_id>', methods=['POST'])
def annuler_rdv(rdv_id):
    """Annuler un rendez-vous"""
    from controllers.rdv_controller import annuler_rdv as annuler_rdv_func
    return annuler_rdv_func(rdv_id)

if __name__ == '__main__':
    app.run(debug=True)
