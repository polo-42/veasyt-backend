from flask.views import MethodView
from flask import jsonify

class BaseView(MethodView):

    notallowed = 'Request not allowed', 405
    notfound = 'Resource not found', 404
    badrequest = 'Bad rquest', 400
    unauthorized = 'Request not authorized', 401
    forbidden = 'Forbidden request', 403
    notacceptable = 'Request not acceptable', 406

    def __init__(self, resource):
        self.resource = resource
    
    def deleted(self, res):
        return self.tojson(res), 204
    
    def tojson(self, element):
        return element.todict()
    
    def sendresponse(self, element):
        if type(element) is self.resource:
            return self.tojson(element)

        elif element == 404:
            return BaseView.notfound

        elif element == 405:
            return BaseView.notallowed
        
        elif element == 400:
            return BaseView.badrequest

        elif element == 401:
            return BaseView.unauthorized
        
        elif element == 403:
            return BaseView.forbidden

        elif element == 406:
            return BaseView.notacceptable    

    def get(self):
        return BaseView.notallowed

    def post(self, data):
        return BaseView.notallowed

    def patch(self, _):
        return BaseView.notallowed
    
    def delete(self, _):
        return BaseView.notallowed    