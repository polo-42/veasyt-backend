from flask import jsonify
from views.BaseView import BaseView

class ElementView(BaseView):

    def __init__(self, resource):
        super().__init__(resource)
    
    def get(self, id):
        element = self.resource.get(id)
        if element == 404 :
            return ElementView.notfound
        
        return self.tojson(element)
    
    def delete(self, id):
        element = self.resource.get(id)
        if element == 404 :
            return ElementView.notfound
        
        res = element.delete()
        if (res):
            return res, 204
        else:
            return ElementView.notallowed

    def patch(self, _):
        return ElementView.notallowed
    
    def post(self, _):
        return ElementView.notallowed