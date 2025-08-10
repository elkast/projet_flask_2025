# DOCUMENTATION COMPLÈTE - APPLICATION GESTION RDV MÉDICAUX
## PRÉSENTATION DÉTAILLÉE POUR SOUTENANCE

---

## 1. INTRODUCTION & OBJECTIF
**Application web complète** de gestion de rendez-vous médicaux développée en **Flask/Python** avec une architecture **MVC** moderne. L'application permet aux patients de prendre, gérer et suivre leurs rendez-vous médicaux en ligne.

---

## 2. ARCHITECTURE TECHNIQUE DÉTAILLÉE

### 2.1 Structure du Projet
```
rdv_medical_app/
├── app.py                    # Point d'entrée principal
├── config.py                 # Configuration de l'application
├── requirements.txt          # Dépendances Python
├── models/                   # Couche Modèle (MVC)
│   ├── __init__.py          # Initialisation SQLAlchemy
│   ├── patient_model.py     # Modèle Patient
│   ├── medecin_model.py     # Modèle Médecin
│   └── rdv_model.py         # Modèle Rendez-vous
├── controllers/             # Couche Contrôleur (MVC)
│   ├── patient_controller.py
│   ├── medecin_controller.py
│   ├── rdv_controller.py
│   └── api_controller.py
├── templates/               # Couche Vue (MVC)
│   ├── base.html           # Template de base
│   ├── index.html          # Page d'accueil
│   ├── patient/            # Templates patients
│   ├── medecins/           # Templates médecins
│   └── rdv/               # Templates rendez-vous
└── static/                # Fichiers statiques
    ├── css/
    └── js/
```

### 2.2 Stack Technique
- **Backend**: Flask 2.x, Python 3.8+
- **ORM**: SQLAlchemy 2.x
- **Base de données**: SQLite (développement) / PostgreSQL (production)
- **Frontend**: Jinja2 templates avec CSS moderne
- **Templates**: Système de templates Jinja2 avec héritage

---

## 3. BASE DE DONNÉES - ANALYSE DÉTAILLÉE

### 3.1 Schéma Relationnel
```sql
-- Table patients
CREATE TABLE patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    date_naissance DATE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table medecins
CREATE TABLE medecin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    specialite VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table rendez_vous
CREATE TABLE rendez_vous (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_heure DATETIME NOT NULL,
    motif TEXT,
    statut VARCHAR(20) DEFAULT 'planifie',
    patient_id INTEGER NOT NULL,
    medecin_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE,
    FOREIGN KEY (medecin_id) REFERENCES medecin(id) ON DELETE CASCADE
);
```

### 3.2 Modèles SQLAlchemy Détaillés

#### 3.2.1 Modèle Patient (patient_model.py)
```python
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Patient(db.Model):
    __tablename__ = 'patient'
    
    # Champs de base
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)
    
    # Méthodes de sécurité
    def set_password(self, password):
        """Hash et stocke le mot de passe"""
        self.mot_de_passe_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.mot_de_passe_hash, password)
```

#### 3.2.2 Modèle Médecin (medecin_model.py)
```python
class Medecin(db.Model):
    __tablename__ = 'medecin'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    rendez_vous = db.relationship('RendezVous', backref='medecin', lazy=True)
```

#### 3.2.3 Modèle Rendez-vous (rdv_model.py)
```python
class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'
    
    id = db.Column(db.Integer, primary_key=True)
    date_heure = db.Column(db.DateTime, nullable=False)
    motif = db.Column(db.Text)
    statut = db.Column(db.String(20), default='planifie')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Méthodes utilitaires
    def is_past(self):
        """Vérifie si le rendez-vous est passé"""
        return self.date_heure < datetime.utcnow()
    
    def can_cancel(self):
        """Vérifie si le rendez-vous peut être annulé"""
        return self.statut == 'planifie' and not self.is_past()
```

---

## 4. SYSTÈME DE ROUTAGE DÉTAILLÉ

### 4.1 Configuration des Routes (app.py)
```python
# Configuration Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///rdv.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db.init_app(app)
```

### 4.2 Routes Principales avec Documentation

#### 4.2.1 Routes Patient
```python
@app.route('/patient/connexion', methods=['GET', 'POST'])
def patient_connexion():
    """
    Gère la connexion des patients
    - GET: Affiche le formulaire de connexion
    - POST: Traite les identifiants et crée la session
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        patient = Patient.query.filter_by(email=email).first()
        
        if patient and patient.check_password(password):
            session['patient_id'] = patient.id
            flash('Connexion réussie!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    
    return render_template('patient/connexion.html')

@app.route('/patient/inscription', methods=['GET', 'POST'])
def patient_inscription():
    """
    Gère l'inscription des nouveaux patients
    Validation des données et création du compte
    """
    if request.method == 'POST':
        # Validation côté serveur
        errors = validate_patient_data(request.form)
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('patient/inscription.html')
        
        # Création du patient
        patient = Patient(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            email=request.form['email'],
            telephone=request.form['telephone'],
            date_naissance=datetime.strptime(request.form['date_naissance'], '%Y-%m-%d')
        )
        patient.set_password(request.form['password'])
        
        db.session.add(patient)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('patient_connexion'))
```

#### 4.2.2 Routes Rendez-vous
```python
@app.route('/rdv/nouveau', methods=['GET', 'POST'])
def nouveau_rdv():
    """
    Création d'un nouveau rendez-vous
    - Affiche le formulaire
    - Traite la soumission
    - Vérifie les disponibilités
    """
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    if request.method == 'POST':
        # Validation de la date
        date_str = request.form['date_heure']
        try:
            date_heure = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            if date_heure < datetime.now():
                flash('La date doit être future', 'danger')
                return render_template('rdv/nouveau.html')
        except ValueError:
            flash('Format de date invalide', 'danger')
            return render_template('rdv/nouveau.html')
        
        # Création du rendez-vous
        rdv = RendezVous(
            date_heure=date_heure,
            motif=request.form['motif'],
            patient_id=session['patient_id'],
            medecin_id=request.form['medecin_id']
        )
        
        db.session.add(rdv)
        db.session.commit()
        
        flash('Rendez-vous créé avec succès!', 'success')
        return redirect(url_for('liste_rdv'))
    
    medecins = Medecin.query.all()
    return render_template('rdv/nouveau.html', medecins=medecins)

@app.route('/rdv/details/<int:rdv_id>')
def rdv_details(rdv_id):
    """
    Affiche les détails d'un rendez-vous
    Vérifie que le patient est propriétaire du RDV
    """
    if 'patient_id' not in session:
        return redirect(url_for('patient_connexion'))
    
    rdv = RendezVous.query.get_or_404(rdv_id)
    
    # Vérification des permissions
    if rdv.patient_id != session['patient_id']:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('liste_rdv'))
    
    return render_template('rdv/details.html', rdv=rdv)
```

---

## 5. SYSTÈME DE TEMPLATES DÉTAILLÉ

### 5.1 Structure des Templates avec Héritage
