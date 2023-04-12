from views.ElementView import ElementView
from views.CollectionView import CollectionView
from views.CatalogueView import CatalogueView
#from db.RoomResource import RoomResource
from db.CatalogueResource import CategoryResource, CatalogueResource

def initendpoint(app, resource, name, ElView = ElementView, ColView = CollectionView):
    initelement(app,resource,name,ElView)
    initcollection(app,resource,name,ColView)

#ELEMENT ENDPOINTS WILL ALWAYS USE DYNAMIC ROUTING (EXCEPT OVERRIDE)
def initelement(app, resource, name, ElView = ElementView):
    elementapi = ElView.as_view(f'{name}-element', resource)
    app.add_url_rule(f'/{name}/<int:id>', view_func=elementapi)

def initcollection(app, resource, name, ColView = CollectionView):
    collectionapi = ColView.as_view(f'{name}-collection', resource)
    app.add_url_rule(f'/{name}/', view_func=collectionapi)

def initendpoints(app):
    #initendpoint(app, RoomResource, 'rooms')

    #SINCE COLLECTION VIEW WAS OVERIDDEN FOR CATALOGUE, AS WE USE AN ARGUMENT "CLASS_" TO FILTER THE COLLECTION VIEW
    #AND SINCE WE USE TWO DIFFERENT RESSOURCES FOR THE SAME ENDPOINT
    #WE MUST INIT THE ELEMENT AND COLLECTION VIEWS SEPARETELY
    initendpoint(app, CatalogueResource, 'catalogue')
    initcollection(app, CategoryResource, 'categories', ColView=CatalogueView)
    initendpoint(app, CategoryResource, 'category')
    