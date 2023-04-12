from views.CollectionView import CollectionView
from flask import request, jsonify

class CatalogueView(CollectionView):

    def __init__(self, resource):
        super().__init__(resource)

    def get(self):
        class_ = request.args['class']
        if class_ == None : CatalogueView.notallowed

        collection = self.resource.getall(class_)

        return [ self.tojson(el) for el in collection ]