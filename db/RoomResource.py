from db.BaseResource import BaseResource
from db.FurnitureResource import FurnitureResource

class RoomResource(BaseResource):

    def __init__(self,id,name,id_load_address,furnitures,width=None,length=None):
        self.id = id
        self.name = name
        self.id_load_address = id_load_address
        self.furnitures = furnitures
        self.width = width
        self.length = length

# override BaseResource
    @staticmethod
    def get(id):
        cursor = RoomResource.db.cursor()
        request = f'SELECT id_piece, nom, id_adresse_chargement FROM Piece WHERE id_piece = {id}'
        cursor.execute(request)
        room = cursor.fetchone()

        if room is None : return RoomResource.notfound

        cursor = RoomResource.db.cursor()
        request = f"""
            SELECT m.id_meuble_client, m.quantite, c.nom_meuble, c.poids, c.largeur, c.longueur, c.hauteur
            FROM Meuble_catalogue AS c, Meuble_client_defaut AS d, Meuble_client AS m
            WHERE m.id_meuble_client = d.id_meuble_client
            AND c.id_meuble_catalogue = d.id_meuble_catalogue
            AND m.id_piece = {id}
        """
        cursor.execute(request)

        furnitures = [FurnitureResource(f[0],f[1],f[2],f[3],f[4],f[5],f[6]) for f in cursor.fetchall()]
        
        return RoomResource(room[0], room[1], room[2], furnitures)
    
    @staticmethod
    def getall():
        cursor = RoomResource.db.cursor()
        request = 'SELECT id_piece FROM Piece'
        cursor.execute(request)

        return filter(
            lambda room : type(room) is RoomResource, 
            [RoomResource.get(r[0]) for r in cursor.fetchall()]
        )
    
    @staticmethod
    def add(data):
        db = RoomResource.db
        cursor = db.cursor()
        request = f"""
            INSERT INTO Piece (nom, id_adresse_chargement) 
            VALUES ('{data['name']}',{data['id_load_address']});
            """
        cursor.execute(request)
        db.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        roomid = cursor.fetchone()[0]
        room = RoomResource.get(roomid)

        return room

    def delete():
        return RoomResource.notallowed
    
    def todict(self):
        return {
            'id': self.id,
            'name': self.name,
            'id_load_adress': self.id_load_address,
            'furnitures': [f.todict() for f in self.furnitures]
        }
    
# additionnal functionalities
    def getvolume(self):
        return sum([f.getvolume() for f in self.furnitures])