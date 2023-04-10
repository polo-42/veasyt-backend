from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from db.furniture import FurnitureDefault

inventory_endpoint = Blueprint('inventory', __name__)

@inventory_endpoint.route('/', methods=['POST'])
@cross_origin()
def insertInventoryAPI():
    if request.method == 'POST':
        furniture = FurnitureDefault.fromjson(request.json)
        id_furniture = furniture.save()
        return jsonify(id_furniture), 201


@inventory_endpoint.route('/<id_furniture>', methods=['DELETE'])
@cross_origin()
def removeInventoryAPI(id_furniture):
    if request.method == 'DELETE':
        result = FurnitureDefault.delete(id_furniture)
        return 'Furniture deleted', 204
    
    #else :
    #    rooms = Room.getAll('id_adresse_chargement = 4')
    #    return jsonify([room.todict() for room in rooms]), 200
    
    #TODO: 