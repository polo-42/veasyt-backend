import mysql.connector, json
from db.base import baseModel

mydb = mysql.connector.connect(
    host="amenitydev-veasyt.mysql.database.azure.com",
    user="amenitydev",
    password="woYASh$7$B6g866w",
    database="veasyt_db"
)
cursor = mydb.cursor(buffered=True)

class Room(baseModel):    
    
    def __init__(self,id,name,id_load_address,width=None,length=None):
        self.id = id
        self.name = name
        self.width = width
        self.length = length
        self.id_load_address = id_load_address
    
    def save(self):
        request = f"""
            INSERT INTO Piece (nom, id_adresse_chargement) 
            VALUES ('{self.name}',{self.id_load_address});
            """
        cursor.execute(request)
        mydb.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        return cursor.fetchone()[0]

    
    def todict(self):
        return {k: v for k, v in vars(self).items() if v is not None}

    @staticmethod
    def getAll(filter=None):
        request = 'SELECT id_piece, nom, id_adresse_chargement FROM Piece'
        if filter is not None : 
            request += f' WHERE {filter}'

        cursor.execute(request)
        return [
            Room.fromdb(room)
            for room in cursor.fetchall()
        ]

    @staticmethod
    def fromjson(data):
        """init from json data"""
        room = Room(None,data['name'],id_load_address=data['id_load_address'])
        return room

    @staticmethod
    def fromdb(row):
        """init from db data"""
        room = Room(row[0], row[1], row[2])
        return room
    
    @staticmethod
    def getAllFurniture(idRoom):
        request = f"""
        SELECT catalogue.nom_meuble, furniture.quantite, catalogue.largeur, catalogue.longueur, catalogue.hauteur
        FROM Meuble_catalogue AS catalogue, Meuble_client_defaut AS occurence, Meuble_client AS furniture
        WHERE furniture.id_meuble_client = occurence.id_meuble_client
        AND catalogue.id_meuble_catalogue = occurence.id_meuble_catalogue
        AND furniture.id_piece = {idRoom}
        """
        cursor.execute(request)
        furnitures = [{'furniture_name':f[0], 'quantity': f[1], "volume":((f[2]*f[3]*f[4])/1000000)} for f in cursor.fetchall()]

        request = f"SELECT Piece.nom FROM Piece WHERE Piece.id_piece = {idRoom}"
        cursor.execute(request)
        object = cursor.fetchone()
        
        total_volume = 0
        for furniture in furnitures:
            total_volume += furniture["volume"]
        return {
            'room_name': object[0],
            'furnitures': furnitures,
            "total_volume": total_volume
            }

    @staticmethod
    def getTotalVolume(idRoom):
        pass