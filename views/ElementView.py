from flask import jsonify, request
from views.BaseView import BaseView

class ElementView(BaseView):

    def __init__(self, resource):
        super().__init__(resource)
    
    def get(self, id):
        element = self.resource.get(id)
        
        return self.sendresponse(element)
    
    def delete(self, id):
        element = self.resource.get(id)
        if element == 404 :
            return ElementView.notfound
        
        res = element.delete()
        return self.sendresponse(res)

    def patch(self, id):
        element = self.resource.get(id)
        if element == 404 :
            return ElementView.notfound
    
        element = element.update(request.json)
        return self.sendresponse(element)
        
    
    def post(self, data):
        element = self.resource.add(data)
        return self.sendresponse(element)