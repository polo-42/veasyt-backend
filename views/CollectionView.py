from flask import jsonify
from views.BaseView import BaseView

class CollectionView(BaseView):

    def __init__(self, resource):
        super().__init__(resource)

    def get(self):
        collection = self.resource.getall()

        return [ self.tojson(el) for el in collection ]

    def post(self, data):
        dictdata = jsonify(data)
        element = self.resource.add(dictdata)
        
        if type(element) is self.resource:
            return self.tojson(element)
        
        elif element == 404:
            return CollectionView.notfound
        
        elif element == 405:
            return CollectionView.notallowed

    def patch(self, _):
        return CollectionView.notallowed
    
    def delete(self, _):
        return CollectionView.notallowed