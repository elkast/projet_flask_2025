# DOCUMENTATION COMPLÈTE — Application de gestion de rendez‑vous médicaux

**Nom du projet :** RDV Médicaux — `rdv_medical_app`

**Version :** 1.0

**Auteurs :** Aliou, Gnanba Divine, Trahebi Maeva,gogoua , Elkast Orsini

---

## Résumé (version courte pour votre médecin)

Cette application web permet à des patients de créer, gérer et suivre leurs rendez‑vous médicaux en ligne. Elle est développée en **Python** avec le micro‑framework **Flask** et suit l'architecture **MVC** (Modèle — Vue — Contrôleur) pour séparer clairement les données, la logique et l'affichage.

Si vous souhaitez que je vous aide à l'installer ou à la déployer pour que votre médecin puisse l'essayer directement, dites‑le moi — je peux aussi préparer un fichier PDF prêt à être envoyé.

---

## Table des matières

1. Présentation
2. Arborescence du projet
3. Prérequis & installation
4. Lancer l'application
5. Base de données & modèles
6. Routes principales (API / pages)
7. Templates et interface
8. Sécurité et bonnes pratiques
9. Tests simples
10. Foire aux questions (FAQ)
11. Annexes (SQL, extraits de code)

---

## 1. Présentation

**Objectif :** fournir une interface simple pour :

* S'inscrire / se connecter en tant que patient
* Consulter la liste des médecins
* Créer, voir, annuler et consulter les détails des rendez‑vous

**Public ciblé :** patients et médecins d'un cabinet ou d'une clinique souhaitant gérer les RDV de manière simple.

---

## 2. Arborescence du projet

```
rdv_medical_app/
├── app.py                    # Point d'entrée principal
├── config.py                 # Configuration de l'application
├── requirements.txt          # Dépendances Python
├── models/                   # Couche Modèle
│   ├── __init__.py
│   ├── patient_model.py
│   ├── medecin_model.py
│   └── rdv_model.py
├── controllers/              # Couche Contrôleur (routes & logique)
│   ├── patient_controller.py
│   ├── medecin_controller.py
│   ├── rdv_controller.py
│   └── api_controller.py
├── templates/                # Pages HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── patient/
│   ├── medecins/
│   └── rdv/
└── static/                   # CSS, JS, images
    ├── css/
    └── js/
```

**Explication simple pour débutants :**

* `models/` contient les définitions des tables (Patient, Médecin, RendezVous).
* `controllers/` contient les fonctions qui répondent aux URLs (routes) et qui manipulent les modèles.
* `templates/` contient les fichiers HTML qui affichent les pages à l'utilisateur.

---

## 3. Prérequis & installation

### Prérequis

* Python 3.8 ou supérieur
* pip (gestionnaire de paquets Python)

### Installer les dépendances

Ouvrez un terminal, placez‑vous dans le dossier du projet et lancez :

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient généralement : `Flask`, `SQLAlchemy`, `Werkzeug`, etc.

---

## 4. Lancer l'application (mode développement)

Deux méthodes :

### Méthode 1 — Avec `python` (la plus simple)

```bash
python app.py
```

Puis ouvrez votre navigateur à : `http://127.0.0.1:5000`.

### Méthode 2 — Avec `flask run`

Sous Linux/macOS :

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Sous Windows (PowerShell) :

```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
```

> Remarque : la base SQLite (fichier `rdv.db` ou autre selon `config.py`) est généralement créée automatiquement au premier lancement si le projet contient une commande d'initialisation.

---

## 5. Base de données & modèles

L'application utilise SQLAlchemy (ORM) pour définir les tables sous forme de classes Python.

### Schéma simplifié (SQL)

```sql
-- patients
id, nom, prenom, email (unique), telephone, date_naissance, mot_de_passe_hash, created_at

-- medecins
id, nom, prenom, specialite, email (unique), telephone, created_at

-- rendez_vous
id, date_heure, motif, statut, patient_id (FK), medecin_id (FK), created_at
```

### Comportement important des modèles

* Les mots de passe sont **hashés** (on ne stocke jamais le mot de passe en clair). Méthodes : `set_password`, `check_password`.
* `RendezVous` contient des méthodes utilitaires : `is_past()` (est‑ce que le RDV est déjà passé ?) et `can_cancel()` (peut‑on l'annuler ?).

---

## 6. Routes principales (pages et actions importantes)

Voici une liste claire des routes que votre médecin ou un utilisateur peut utiliser :

### Authentification patient

* `GET /patient/connexion` — formulaire de connexion
* `POST /patient/connexion` — traitement de la connexion
* `GET /patient/inscription` — formulaire d'inscription
* `POST /patient/inscription` — création d'un nouveau patient

### Rendez‑vous

* `GET /rdv/nouveau` — affiche le formulaire de création (doit être connecté)
* `POST /rdv/nouveau` — enregistre le rendez‑vous (vérifie la date)
* `GET /rdv/details/<rdv_id>` — affiche le détail d'un RDV (vérifie que le patient est propriétaire)
* `GET /rdv/liste` — liste des rendez‑vous du patient (souvent paginée)
* `POST /rdv/annuler/<rdv_id>` — annule si autorisé

### Médecins

* `GET /medecins` — liste des médecins disponibles
* `GET /medecins/<id>` — fiche détaillée du médecin

> Chaque route renvoie généralement un template HTML (render\_template) ou redirige vers une autre page.

---

## 7. Templates & interface

L'interface utilise Jinja2 — un moteur de templates intégré à Flask. Les templates se basent sur un fichier `base.html` :

* `base.html` : structure HTML commune (header, footer, inclusion CSS/JS)
* Les autres templates héritent de `base.html` et remplissent des blocs (ex : `content`).

**Conseil pour modifier le front :**

* Regarder `templates/base.html` pour les éléments globaux (menu, footer)
* Modifier uniquement les templates dans `templates/patient/`, `templates/rdv/` pour personnaliser les pages.

---

## 8. Sécurité et bonnes pratiques (essentiel pour un projet destiné à un cabinet médical)

1. **Ne pas stocker de mots de passe en clair.** Utiliser `werkzeug.security.generate_password_hash` et `check_password_hash`.
2. **Utiliser HTTPS en production.** Ne pas exposer l'application en HTTP sur internet sans TLS.
3. **Protéger les routes sensibles.** Vérifier `session['patient_id']` avant d'autoriser la création/consultation d'un RDV.
4. **Limiter les erreurs révélant des informations sensibles.** Ne pas afficher de stack trace en production.
5. **Sauvegardes régulières de la base de données.**
6. **Logs et audit.** Garder des logs d'accès/erreurs si le service est en production.

---

## 9. Tests simples (vérifier que tout fonctionne)

1. **Créer un compte patient** via la page d'inscription.
2. **Se connecter** avec ce compte.
3. **Créer un rendez‑vous** (choisir un médecin et une date future).
4. **Vérifier la liste des RDV** et ouvrir une fiche détail.
5. **Tester l'annulation** d'un RDV.

Si une étape échoue, regarder la console du serveur (terminal) pour les erreurs et vérifier `requirements.txt` et la configuration de la base de données dans `config.py`.

---

## 10. FAQ — Questions fréquentes

**Q : Mon médecin peut‑il utiliser l'application sans installer Python ?**
R : Non. Pour exécuter localement, il faut Python. Pour faciliter l'usage, on peut déployer l'application sur un petit serveur (Heroku, Render, OVH, etc.) et fournir une URL.

**Q : Comment partager l'application facilement ?**
R : Déployer sur un service cloud (Render, Railway, Heroku) ou préparer un conteneur Docker pour l'exécuter plus facilement.

**Q : Les données sont‑elles confidentielles ?**
R : En local oui (sur votre machine). En production, il faut ajouter HTTPS, contrôles d'accès, et sauvegardes chiffrées si nécessaire.

---

## 11. Annexes

### A. Extrait du SQL de création des tables

```sql
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

CREATE TABLE medecin (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  specialite VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  telephone VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

### B. Exemple d'utilisation (extrait de code)

**Connexion patient (extrait)**

```python
@app.route('/patient/connexion', methods=['GET', 'POST'])
def patient_connexion():
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
```

---
*Fin de la documentation.*
