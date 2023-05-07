from views.ElementView import ElementView
from views.CollectionView import CollectionView
from views.FilterCollectionView import FilterCollectionView

from resources.RoomResource import RoomResource
from resources.CatalogueResource import CategoryResource, CatalogueResource
from resources.FurnitureResource import FurnitureResource
from resources.AddressResource import AddressResource
from resources.VisitResource import VisitResource

def initendpoint(app, resource, name, ElView = ElementView, ColView = CollectionView):
    initelement(app,resource,name,ElView)
    initcollection(app,resource,name,ColView)

def initelement(app, resource, name, ElView = ElementView):
    elementapi = ElView.as_view(f'{name}-element', resource)
    app.add_url_rule(f'/{name}/<int:id>', view_func=elementapi)

def initcollection(app, resource, name, ColView = CollectionView):
    collectionapi = ColView.as_view(f'{name}-collection', resource)
    app.add_url_rule(f'/{name}/', view_func=collectionapi)

def initendpoints(app):

    initelement(app, CategoryResource, 'categories')
    initcollection(app, CategoryResource, 'categories', ColView=FilterCollectionView)
    
    initelement(app, CatalogueResource, 'catalogue')
    initcollection(app, CatalogueResource, 'catalogue', ColView=FilterCollectionView)

    initelement(app, FurnitureResource, 'furnitures')
    initcollection(app, FurnitureResource, 'furnitures', ColView=FilterCollectionView)

    initendpoint(app, RoomResource, 'rooms') 
    #TODO: FilterCollectionView with address (All the rooms of an addresss)
    #TODO: FilterCollectionView with visit (All the rooms of a visit)
    
    initelement(app, AddressResource, 'addresses')
    initcollection(app, AddressResource, 'addresses', ColView=FilterCollectionView)

    initendpoint(app, VisitResource, 'visits')
    #TODO: FilterCollectionView with client (All the visits of a client)
    
