from views.ElementView import ElementView
from views.CollectionView import CollectionView
from db.RoomResource import RoomResource

def initendpoint(app, resource, name, ElView = ElementView, ColView = CollectionView):
    collectionapi = ColView.as_view(f'{name}-collection', resource)
    app.add_url_rule(f'/{name}/', view_func=collectionapi)
    elementapi = ElView.as_view(f'{name}-element', resource)
    app.add_url_rule(f'/{name}/<int:id>', view_func=elementapi)

def initendpoints(app):
    initendpoint(app, RoomResource, 'rooms')