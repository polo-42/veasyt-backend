from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from db.room import Room

rooms_endpoint = Blueprint('rooms', __name__)

@rooms_endpoint.route('/', methods=['GET','POST'])
@cross_origin()
def roomsAPI():
    if request.method == 'GET':
        id = request.args['id_load_address']
        rooms = Room.getAll(f'id_adresse_chargement = {id}')
        return jsonify([room.todict() for room in rooms]), 200
    else:
        room = Room.fromjson(request.json)
        idroom = room.save()
        return jsonify(idroom), 200

@rooms_endpoint.route('/<idroom>')
@cross_origin()
def roomAPI(idroom):
    furnitures = Room.getAllFurniture(idroom)
    return jsonify(furnitures), 200


    #/rooms/id_token=fnslijfosdjfa&id_address = 4
    #
#TODO: New endpoint with id_address
#TODO: New endpoint with id_room




