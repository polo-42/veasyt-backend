from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from db.address import Address_postal

addressesPostal_endpoint = Blueprint('addressesPostal', __name__)

@addressesPostal_endpoint.route('/', methods=['POST'])
@cross_origin()
def insertAdressPostalAPI():
    if request.method == 'POST':
        address_postal = Address_postal.fromjson(request.json)
        id_address_postal = address_postal.save()
        return jsonify(id_address_postal), 201