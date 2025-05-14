from flask_restful import Api
from .. import app,BASE_API
from .farmacia import Farmacia

api = Api(app)

# Registro de las APIs 
api.add_resource(Farmacia, f"{BASE_API}/farmacias", f"{BASE_API}/farmacias/<int:id>")