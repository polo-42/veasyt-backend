from views.ElementView import ElementView
from db.RoomResource import RoomResource

def initendpoint(app, resource, name):
    elementapi = ElementView.as_view(f'{name}-element', resource)
    app.add_url_rule(f'/{name}/<int:id>', view_func=elementapi)

def initendpoints(app):
    initendpoint(app, RoomResource, 'rooms')