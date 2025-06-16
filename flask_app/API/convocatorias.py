import marshmallow.exceptions
from .. import app, db
from ..models import Convocatoria, Listado, Farmacia
from ..schemas import ConvocatoriaSchema, ListadoSchema, TIPOS_LISTADO_SCHEMAS
from . import BASE_API
from flask_jwt_extended import jwt_required
from flask import request
import sqlalchemy
import marshmallow

@app.get(f"{BASE_API}/convocatorias")
@jwt_required()
def api_get_convocatorias():
   # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#order-by
   convocatorias = Convocatoria.query.order_by(Convocatoria.fecha_ini.desc()).all()

   return { "data": ConvocatoriaSchema(many=True).dump(convocatorias) }



