import mysql.connector
from db.base import baseModel

mydb = mysql.connector.connect(
    host="amenitydev-veasyt.mysql.database.azure.com",
    user="amenitydev",
    password="woYASh$7$B6g866w",
    database="veasyt_db"
)

cursor = mydb.cursor(buffered=True)

#TODO: CREATE TABLE FOR MULTIPLE CATEGORIES

class Furniture(baseModel):
    def __init__(self,id,quantity,name,weight,width,length,height):
        self.id = id
        self.quantity = quantity
        self.name = name
        self.weight = weight
        self.dimension = (width,length,height)
    
    def todict(self):
        return {k: v for k, v in vars(self).items() if v is not None}

class FurnitureDefault(Furniture):
    def __init__(self,id,quantity,name,weight,width,length,height,id_catalogue,id_room,id_unload_address):
        super().__init__(id,quantity,name,weight,width,length,height)
        self.id_catalogue = id_catalogue
        self.id_room = id_room
        self.id_unload_address = id_unload_address
    
    @staticmethod
    def fromjson(data): #createObjectFromJson
        cursor.execute(f"""
        SELECT nom_meuble, poids, largeur, longueur, hauteur, icone 
        FROM Meuble_catalogue
        WHERE id_meuble_catalogue = {data["id_catalogue"]}
        """)

        object =  cursor.fetchone()
        furniture = FurnitureDefault(None, data["quantity"], object[0], object[1], object[2], object[3], object[4], data["id_catalogue"], data["id_room"], data["id_unload_address"])
        return furniture
    
    def save(self):
        request = f"""
        INSERT INTO Meuble_client (est_avance, quantite, id_piece, id_adresse_dechargement) VALUES (0, {self.quantity}, {self.id_room}, {self.id_unload_address})   
        """
        cursor.execute(request)
        mydb.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')      
        id_furniture = cursor.fetchone()[0]
        # cursor.fetchall() au cas ou il y a une erreur

        request = (f"""
        INSERT INTO Meuble_client_defaut (id_meuble_client, id_meuble_catalogue) VALUES ({id_furniture}, {self.id_catalogue})
        """)
        cursor.execute(request)
        mydb.commit()
        return id_furniture
    
    def getAll():
        pass

class FurnitureCustom(Furniture):
    def __init__(self,id,quantity,name,weight,width,length,height,id_catalogue,id_room,id_unload_address):
        super().__init__(id,quantity,name,weight,width,length,height)
        self.id_catalogue = id_catalogue
        self.id_room = id_room
        self.id_unload_adress = id_unload_address
        #TODO: Add remaining attributes
        pass
    
    def save(self):
        pass

class FurnitureCatalogue():
    @staticmethod
    def getAll(filter = None):
        result = []
        cursor.execute("SELECT id_categorie, nom_categorie FROM Meuble_categorie")
        categories = cursor.fetchall()

        for (id_category, category_name) in categories:
            cursor.execute(f"""
                SELECT Meuble_catalogue.id_meuble_catalogue, nom_meuble, icone 
                FROM Meuble_catalogue, Meuble_categories 
                WHERE Meuble_catalogue.id_meuble_catalogue = Meuble_categories.id_meuble_catalogue
                AND Meuble_categories.id_categorie = {id_category}""")
            
            result.append({
                "id_category" : id_category,
                "category_name" : category_name,
                "furnitures" : [{'id':f[0], 'name': f[1], 'iconPath': f[2]} for f in cursor.fetchall()]
            })
            
        return result





























































