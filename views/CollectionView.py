from flask import jsonify, request
from views.BaseView import BaseView

class CollectionView(BaseView):

    def __init__(self, resource):
        super().__init__(resource)

    def get(self):
        collection = self.resource.getall()

        return [ self.tojson(el) for el in collection ]

    #ALL COLLECTIONS MUST HAVE AN ADD FUNCTION THAT IS APPLIED TO THE CLASS (STATIC METHOD), THIS WAY WE CAN CALL THE ADD METHOD FOR ALL THE COLLECTION ENDPOINTS EXCEPT OVERRIDES
    def post(self):
        element = self.resource.add(request.json)
        
        if type(element) is self.resource:
            return self.tojson(element)
        
        elif element == 404:
            return CollectionView.notfound
        
        elif element == 405:
            return CollectionView.notallowed

