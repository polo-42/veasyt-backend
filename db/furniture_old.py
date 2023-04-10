import mysql.connector, json
from db.base import baseModel

mydb = mysql.connector.connect(
    host="amenitydev-veasyt.mysql.database.azure.com",
    user="amenitydev",
    password="woYASh$7$B6g866w",
    database="veasyt_db"
)

cursor = mydb.cursor(buffered=True)

class furniture_client(baseModel):
    def __init__(self,id,type,is_advanced=0,quantity=-1,id_room=-1,id_unload_address=-1):
        self.id = id
        self.type = type
        self.is_advanced = is_advanced
        self.quantity = quantity
        self.id_room = id_room
        self.id_unload_address = id_unload_address

    def save(self):
        request = f"""
            INSERT INTO Meuble_client (nom, largeur, longueur, id_adresse_chargement) 
            VALUES ('{self.id}',{self.type},{self.is_advanced},{self.quantity},{self.id_room},{self.id_unload_address});
            """
        cursor.execute(request)
        mydb.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        return cursor.fetchone()[0]
    
    def todict(self):
        return {k: v for k, v in vars(self).items() if v is not None}    
    


    @staticmethod
    def getAll(filter=None):
        request = 'SELECT id_meuble_client, nom FROM Meuble_client'
        if filter is not None : 
            request += f' WHERE {filter}'

        cursor.execute(request)
        return [
            Room.fromdb(room)
            for room in cursor.fetchall()
        ]

## getAll(filter)
## save

#class furniture_client(baseModel):
#    def __init__(self,id,type,is_advanced=0,weight=-1,width=-1,height=-1,id_load_address=-1):
#        self.id = id
#        self.type = type
#        self.is_advanced = is_advanced
#        self.weight = weight
#        self.width = width
#        self.height = height
#        self.id_load_adress = id_load_adress

class Furniture_catalogue(baseModel):
    def __init__(self,id,name,type,id_category,weight=None,width=None,length=None,height=None,icon=None):
        self.id = id
        self.name = name
        self.type = type
        self.id_category = id_category
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.icon = icon

    def save(self):
        request = f"""
            INSERT INTO Meuble_catalogue (nom, type, poids, largeur, longueur, hauteur, icone, id_categorie) 
            VALUES ('{self.name}','{self.type}',{self.weight},{self.width},{self.length},{self.height},'{self.icon}',{self.id_category});
            """
        cursor.execute(request)
        mydb.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        return cursor.fetchone()[0]
    
    def todict(self):
        return {k: v for k, v in vars(self).items() if v is not None}
    
    @staticmethod
    def getAll(filter=None):
        request = 'SELECT id_meuble_catalogue, nom, type, poids, largeur, longueur, hauteur, icone, id_categorie FROM Meuble_catalogue'
        if filter is not None : 
            request += f' WHERE {filter}'

        cursor.execute(request)
        return [
            Furniture_catalogue.fromdb(room)
            for room in cursor.fetchall()
        ]

## getAll(filter)
## save

