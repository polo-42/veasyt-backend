from views.CollectionView import CollectionView
from resources.BaseResource import BaseResource
from flask import request

class FilterCollectionView(CollectionView):

    def __init__(self, resource):
        super().__init__(resource)

    def get(self):
        key = [key for key in request.args if 'filterBy' in key]
        filter = None
        if len(key) >= 1:
            filter = request.args[key[0]]

        if filter == None : return FilterCollectionView.notallowed

        collection = self.resource.getall(filter)

        return [ 
            self.tojson(el) for el in collection 
        ]