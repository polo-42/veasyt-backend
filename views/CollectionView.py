from flask import jsonify, request
from views.BaseView import BaseView
from resources.BaseResource import BaseResource

class CollectionView(BaseView):

    def __init__(self, resource):
        super().__init__(resource)

    def get(self):
        collection = self.resource.getall()

        return [ 
            self.tojson(el) for el in collection 
        ]

    def post(self):
        element = self.resource.add(request.json)
        
        if type(element) is self.resource:
            return self.tojson(element)
        
        elif element == 404:
            return CollectionView.notfound
        
        elif element == 405:
            return CollectionView.notallowed

