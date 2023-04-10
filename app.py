from flask import Flask
from endpoints.rooms import rooms_endpoint
from endpoints.catalogue import catalogue_endpoint

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(rooms_endpoint,url_prefix='/rooms')
app.register_blueprint(catalogue_endpoint,url_prefix='/catalogue')