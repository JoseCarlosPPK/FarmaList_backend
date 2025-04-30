from . import ma
from .models import Centro, Farmacia, FarmaciaHospitalaria, Convocatoria, Tutoriza, Persona, Usuario
from marshmallow import fields

# Schemas marshmellow SqlAlchemy
# Para anidar schemas de forma bidireccional:
# https://marshmallow.readthedocs.io/en/stable/nesting.html?utm_source=chatgpt.com#two-way-nesting

class PersonaSchema(ma.SQLAlchemyAutoSchema):
    centros = fields.List(fields.Nested("CentroSchema", exclude=["personas"]))
    class Meta:
        model = Persona
        load_instance = True
        ordered = False

class CentroSchema(ma.SQLAlchemyAutoSchema):
    personas = fields.List(fields.Nested("PersonaSchema", exclude=["centros"]))
    class Meta:
        model = Centro
        load_instance = True
        ordered = False

# Hereda de CentroSchema para que tenga la relación con Persona
class FarmaciaSchema(CentroSchema):
    class Meta:
        model = Farmacia
        load_instance = True
        ordered = False
        include_fk = True

# Hereda de CentroSchema para que tenga la relación con Persona
class FarmaciaHospitalariaSchema(CentroSchema):
    class Meta:
        model = FarmaciaHospitalaria
        load_instance = True
        ordered = False
        include_fk = True


class ConvocatoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Convocatoria
        load_instance = True
        ordered = False


class TutorizaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tutoriza
        load_instance = True
        ordered = False
        include_fk = True

    
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        ordered = False

