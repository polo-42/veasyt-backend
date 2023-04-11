from flask.views import MethodView
from flask import jsonify

class BaseView(MethodView):

    notallowed = 'Request not allowed', 405
    notfound = 'Resource not found', 404

    def __init__(self, resource):
        self.resource = resource
    
    def deleted(self, res):
        return self.tojson(res), 204
    
    def tojson(self, element):
        return jsonify(element.todict())