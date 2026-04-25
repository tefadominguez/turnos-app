from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    rol = db.Column(db.String(20))  # admin o usuario

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10))
    hora = db.Column(db.String(5))
    cliente = db.Column(db.String(100))
    estado = db.Column(db.String(20), default="activo")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))