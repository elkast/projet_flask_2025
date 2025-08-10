from flask import render_template, request, redirect, url_for, flash, session
from models import patient_model, rdv_model
from werkzeug.security import generate_password_hash, check_password_hash

def index():
    return render_template("index.html")

def patient_inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        date_naissance = request.form['date_naissance']
        telephone = request.form['telephone']

        hashed_password = generate_password_hash(mot_de_passe, method='pbkdf2:sha256')

        if patient_model.get_patient_by_email(email):
            flash('Cet email est déjà enregistré.', 'danger')
            return redirect(url_for('patient_inscription'))

        patient_id = patient_model.create_patient(nom, prenom, email, hashed_password, date_naissance, telephone)
        if patient_id:
            flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('patient_connexion'))
        else:
            flash('Une erreur est survenue lors de l\'inscription.', 'danger')

    return render_template('patient/inscription.html')

def patient_connexion():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        patient = patient_model.get_patient_by_email(email)

        if patient and check_password_hash(patient['mot_de_passe'], mot_de_passe):
            session['patient_id'] = patient['id']
            flash('Connexion réussie!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('patient/connexion.html')

def patient_deconnexion():
    session.pop('patient_id', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

def patient_dashboard():
    if 'patient_id' not in session:
        flash('Veuillez vous connecter pour accéder à votre tableau de bord.', 'warning')
        return redirect(url_for('patient_connexion'))
    
    patient = patient_model.get_patient_by_id(session['patient_id'])
    rendez_vous = rdv_model.get_rdv_by_patient_id(session["patient_id"])

    return render_template('patient/dashboard.html', patient=patient, rendez_vous=rendez_vous)

def patient_profil():
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    patient = patient_model.get_patient_by_id(session['patient_id'])

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        date_naissance = request.form['date_naissance']
        telephone = request.form['telephone']

        if patient_model.update_patient(session['patient_id'], nom, prenom, email, date_naissance, telephone):
            flash('Profil mis à jour avec succès!', 'success')
        else:
            flash('Une erreur est survenue lors de la mise à jour du profil.', 'danger')
        return redirect(url_for('patient_profil'))

    return render_template('patient/profil.html', patient=patient)


