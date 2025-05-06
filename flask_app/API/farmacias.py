import sqlalchemy.exc
from .. import app, db
from ..models import Farmacia, Persona
from ..schemas import FarmaciaSchema, PersonaSchema
from . import BASE_API
from flask import jsonify, request
from flask_jwt_extended import jwt_required
import marshmallow
import sqlalchemy

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
    



@app.post(f"{BASE_API}/farmacias")
@jwt_required()
def api_add_farmacia():
    farmacia_schema = FarmaciaSchema()

    # Con load se validan los datos
    try:
        farmacia = farmacia_schema.load(request.json)
    except marshmallow.ValidationError as e:
        # En e.messages se muestran los errores por cada atributo. Por ejemplo:
        #{ 'nombre': falta y es obligatorio }
        return jsonify(e.messages), 400


    # Intentamos añadir y guardar la farmacia en la BD.
    # Puede haber errores como incumplir restricciones de la BD
    try:            
        db.session.add(farmacia)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return jsonify({'error': e._message()}), 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8


    return jsonify({'msg': 'Farmacia creada', 'farmacia': farmacia_schema.dump(farmacia)}), 201



@app.put(f"{BASE_API}/farmacias/<int:id>")
@jwt_required()
def api_edit_farmacia(id):
    farmacia_schema = FarmaciaSchema(partial=True)
    farmacia = Farmacia.query.get(id)

    if (not farmacia):
        return jsonify({'error': f"Farmacia con id {id} no encontrada"}), 404

    # Con load se validan los datos
    try:
        farmacia = farmacia_schema.load(request.json, instance=farmacia)
    except marshmallow.ValidationError as e:
        # En e.messages se muestran los errores por cada atributo. Por ejemplo:
        #{ 'nombre': falta y es obligatorio }
        return jsonify(e.messages), 400


    # Intentamos editar guardando la farmacia en la BD.
    # https://flask-sqlalchemy.readthedocs.io/en/stable/queries/#insert-update-delete
    # Puede haber errores como incumplir restricciones de la BD
    try:            
       
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return jsonify({'error': e._message()}), 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8


    return jsonify({'msg': 'Farmacia editada', 'farmacia': farmacia_schema.dump(farmacia)}), 201


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