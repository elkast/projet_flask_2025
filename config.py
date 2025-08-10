import os

SECRET_KEY = os.urandom(24)

# Configuration MariaDB
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Modifier selon votre configuration
    'password': '',   # Modifier selon votre configuration
    'database': 'rdv_m',
    'port': 3306,
    'charset': 'utf8mb4'
}

# Configuration SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

