from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
env_file = find_dotenv('.env.development')
if env_file:
    load_dotenv(env_file)
else:
    print("El archivo con variables de ambiente no se encontro.")

# App variables
APP_DEBUG = os.environ.get("FLASK_DEBUG") or 0
APP_PORT = os.environ.get("CONFIG_PORT") or 5000

# Database variables
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_HOST = os.environ.get("POSTGRES_HOST")
STATIC_TOKEN = os.environ.get("STATIC_TOKEN", 'static_token')

# Create database URL
DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Print the database URL
print("DATABASE_URL:", DATABASE_URL)

database = SQLAlchemy()

def init_db(app):
    environment = os.getenv("ENVIRONMENT")
    if environment == "test":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    elif environment == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    else:
        raise ValueError("Unsupported database configuration")

    database.init_app(app)

    with app.app_context():
        database.create_all()

def config_app(app):
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app_context = app.app_context()
    app_context.push()
