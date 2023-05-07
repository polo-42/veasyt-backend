from resources.CatalogueResource import CategoryResource, CatalogueResource
from flask import Flask, render_template
import requests
import json
from endpoints import initendpoints

app = Flask(__name__)
app.config.from_object('config.Config')

initendpoints(app)

@app.route("/inventory", methods=['GET'])
def getInventory():

    #url = "http://127.0.0.1:5000/categories/?filterByClass=typeMeuble"
    url = "http://127.0.0.1:5000/categories/3"
    data = requests.get(url)
    response = data.json()

    recap = {}
    url2 = "http://127.0.0.1:5000/rooms/1"
    data2 = requests.get(url2)
    room = data2.json()
    recap["furniture"] = []
    
    for furniture in room["furnitures"]:
        id_cat = int(furniture["id_catalogue"])
        data3 = requests.get(f"http://127.0.0.1:5000/catalogue/{id_cat}")
        el = data3.json()
        furniture = {}
        for k, v in el.items():
            if k == "id":
                furniture[k] = v
                furniture["keyFrontEnd"] = "btn"+str(v)
            furniture[k] = v
        recap["furniture"].append(furniture)
    
    #for el in newObj["furniture"]:
    #    print(el["name"])

    return render_template("index.html", response=response, recap=recap)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


