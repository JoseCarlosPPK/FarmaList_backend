from . import app, db
from sqlalchemy import desc
from argon2 import PasswordHasher

#Sirve para cargar el schema de la BD si ya tenía tablas creadas
with app.app_context():
    db.reflect()

###############################################################################
# Modelos
###############################################################################
# https://flask-sqlalchemy.readthedocs.io/en/stable/models/#reflecting-tables
class Centro(db.Model):
    __table__ = db.metadata.tables["Centro"]
    personas = db.relationship('Persona', secondary='Tutoriza', back_populates="centros")



class Farmacia(Centro):
    __table__ = db.metadata.tables["Farmacia"]


class FarmaciaHospitalaria(Centro):
    __table__ = db.metadata.tables["Farmacia_hospitalaria"]


class Convocatoria(db.Model):
    __table__ = db.metadata.tables["Convocatoria"]

    def get_n_ultimas_convocatorias(n:int):
        """
        Devuelve las n últimas convocatorias, que son aquellas que tienen
        la fecha inicial mayor

        Args:
            n (int): Cantidad de convocatorias a recuperar

        Returns:
            List: Lista de las n últimas convocatorias
        """
        return Convocatoria.query.order_by(desc(Convocatoria.fecha_ini)).limit(n).all()


class Tutoriza(db.Model):
    __table__ = db.metadata.tables["Tutoriza"]


class Persona(db.Model):
    __table__ = db.metadata.tables["Persona"]
    centros = db.relationship('Centro', secondary='Tutoriza', back_populates="personas")



class Usuario(db.Model):
    __table__ = db.metadata.tables["Usuario"]

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            self.password = PasswordHasher(encoding="utf-8").hash(kwargs['password'])
            del kwargs['password']

        for key, value in kwargs.items():
            setattr(self, key, value)

