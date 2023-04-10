from flask import Blueprint, jsonify
from flask_cors import cross_origin

from db.furniture import FurnitureCatalogue

catalogue_endpoint = Blueprint('catalogue', __name__)

@catalogue_endpoint.route('/', methods=['GET'])
@cross_origin()
def catalogueAPI():
    catalogue = FurnitureCatalogue.getAll()
    return jsonify(catalogue), 200