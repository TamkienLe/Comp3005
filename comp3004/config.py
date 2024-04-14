import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Batgioi99@localhost/fitnessclub'
    SQLALCHEMY_TRACK_MODIFICATIONS = False