from flask import Flask
from endpoints import initendpoints

app = Flask(__name__)
app.config.from_object('config.Config')

initendpoints(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)