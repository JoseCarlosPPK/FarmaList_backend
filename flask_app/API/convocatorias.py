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



@app.delete(f"{BASE_API}/convocatorias/<int:id>")
@jwt_required()
def api_delete_convocatoria(id):
   a_borrar = Convocatoria.query.get(id)

   if (not a_borrar):
      return {"error": f"No hay ninguna convocatoria con id {id}"}, 404

   try:
      db.session.delete(a_borrar)
      db.session.commit()
   except Exception as e:
      return {"error": f"Fallo del servidor al realizar el borrado de la convocatoria con id {id}"}, 500

   return {"msg": f"Centro con id {id} borrado"}, 200 # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/DELETE


