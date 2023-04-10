from flask.views import MethodView

class BaseView(MethodView):

    notallowed = 'Request not allowed', 405
    notfound = 'Resource not found', 404

    def __init__(self, resource):
        self.resource = resource
    
    def deleted(res):
        return res, 204