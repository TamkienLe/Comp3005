from flask import Flask
from .models import db
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a_very_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Batgioi99@localhost/fitnessclub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Set a secret key for session management
    app.secret_key = os.urandom(16)  # Generates a random key each time the app starts; not ideal for production

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app