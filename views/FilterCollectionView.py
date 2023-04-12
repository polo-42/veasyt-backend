from views.CollectionView import CollectionView
from flask import request

class FilterCollectionView(CollectionView):

    def __init__(self, resource):
        super().__init__(resource)

    def get(self):
        filter = request.args[
            [key for key in request.args if 'filterBy' in key][0]
        ]
        if filter == None : FilterCollectionView.notallowed

        collection = self.resource.getall(filter)

        return [ self.tojson(el) for el in collection ]