import os

class Config:
    SECRET_KEY = 'clave_secreta_demo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///turnos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False