import config
from flask import Flask
from endpoints.rooms import rooms_endpoint
from endpoints.catalogue import catalogue_endpoint
from endpoints.furnitures import inventory_endpoint

app = Flask(__name__)
app.config.from_object('config.Config')
print(app.config['DB_USER'])

app.register_blueprint(rooms_endpoint,url_prefix='/rooms')
app.register_blueprint(catalogue_endpoint,url_prefix='/catalogue')
app.register_blueprint(inventory_endpoint,url_prefix='/inventory')

if __name__ == "__main__":
    app.run(host='0.0.0.0')