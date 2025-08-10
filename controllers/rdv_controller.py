from flask import render_template, request, redirect, url_for, flash, session
from models import rdv_model, patient_model
from models.medecin_model import get_medecins as lister_medecins
from models.rdv_model import create_rdv, get_rdv_by_id, cancel_rdv
from datetime import datetime

def nouveau_rdv():
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    medecins = lister_medecins()

    if request.method == 'POST':
        date_heure_str = request.form['date_heure']
        motif = request.form['motif']
        medecin_id = request.form['medecin_id']
        patient_id = session['patient_id']

        try:
            date_heure = datetime.strptime(date_heure_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Format de date et heure invalide.', 'danger')
            return redirect(url_for('nouveau_rdv'))

        if create_rdv(date_heure, motif, patient_id, medecin_id):
            flash('Rendez-vous pris avec succès!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Une erreur est survenue lors de la prise de rendez-vous.', 'danger')

    return render_template('rdv/nouveau.html', medecins=medecins)

def liste_rdv():
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    from models.rdv_model import get_rdv_by_patient_id
    rendez_vous = get_rdv_by_patient_id(session['patient_id'])
    return render_template('rdv/liste.html', rendez_vous=rendez_vous)

def details_rdv(rdv_id):
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    rdv = get_rdv_by_id(rdv_id)

    if not rdv or rdv['patient_id'] != session['patient_id']:
        flash('Rendez-vous introuvable ou vous n\'avez pas les permissions nécessaires.', 'danger')
        return redirect(url_for('liste_rdv'))

    return render_template('rdv/details.html', rdv=rdv)

def annuler_rdv(rdv_id):
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    rdv = get_rdv_by_id(rdv_id)

    if not rdv or rdv['patient_id'] != session['patient_id']:
        flash('Rendez-vous introuvable ou vous n\'avez pas les permissions nécessaires.', 'danger')
        return redirect(url_for('liste_rdv'))

    if request.method == 'POST':
        if cancel_rdv(rdv_id):
            flash('Rendez-vous annulé avec succès.', 'success')
        else:
            flash('Une erreur est survenue lors de l\'annulation du rendez-vous.', 'danger')
    
    return redirect(url_for('liste_rdv'))

