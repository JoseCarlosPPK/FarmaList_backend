from .. import app, db
from ..models import Farmacia, Persona
from ..schemas import FarmaciaSchema
from . import BASE_API
from flask import jsonify, request
from flask_jwt_extended import jwt_required


filter_to_column = {
    "nombre": Farmacia.nombre,
    "personas": Farmacia.personas,
    "correo": Farmacia.correo,
    "cp": Farmacia.cp,
    "direccion": Farmacia.direccion,
    "localidad": Farmacia.localidad,
    "provincia": Farmacia.provincia,
    "movil": Farmacia.movil,
    "telefono": Farmacia.telefono
}

@app.get(f"{BASE_API}/farmacias")
@jwt_required()
def api_get_farmacias():    
    # El método paginate usa los siguientes query params por defecto
    # - page = 1
    # - per_page = 20
    # - max_per_page = None
    # Ver: https://flask-sqlalchemy.readthedocs.io/en/stable/pagination/

    search_query = request.args.get("search", None)
    filter_query = request.args.get("filter", "nombre")
    columna = filter_to_column.get(filter_query, None)

    # Usamos try catch si columna es igual a None
    try:
        if search_query:
            if filter_query != "personas":
                pag_obj = Farmacia.query.filter(columna.ilike(f'%{search_query}%')).paginate(count=True)
            else:
                pag_obj = db.session.query(Farmacia).join(Farmacia.personas).filter(Persona.nombre.ilike(f'%{search_query}%')).distinct().paginate(count=True)

        else:
            pag_obj = Farmacia.query.paginate(count=True)

        farmacias = pag_obj.items
        total = pag_obj.total
        
    except Exception as e:
        farmacias = []
        total = 0

    response = jsonify(
        {
            "data": FarmaciaSchema(many=True).dump(farmacias),
            "total": total
        })
   
    return response
    
    

@app.delete(f"{BASE_API}/farmacias/<int:id>")
@jwt_required()
def api_delete_farmacia(id):

    a_borrar = Farmacia.query.get(id)
 
    if (not a_borrar):
        return jsonify({"error": f"No hay ninguna farmacia con id {id}"}), 404

    try:
        db.session.delete(a_borrar)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Fallo del servidor al realizar el borrado de la farmacia con id {id}"}), 500

    return jsonify({"msg": f"Farmacia con id {id} borrada"}), 200 # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/DELETE