from resources.BaseResource import BaseResource
from resources.FurnitureResource import FurnitureResource

#TODO: ADD A VOLUME ATTRIBUTE TO THE ROOM, BEST SOLUTION TO ADD GENERIC VOLUME ?

class RoomResource(BaseResource):

    def __init__(self,id,name,id_load_address,furnitures,width=None,length=None):
        self.id = id
        self.name = name
        self.id_load_address = id_load_address
        self.furnitures = furnitures
        self.width = width
        self.length = length

    @staticmethod
    def get(id):
        cursor = RoomResource.db.cursor()
        request = f'SELECT id_piece, nom, id_adresse_chargement FROM Piece WHERE id_piece = {id}'
        cursor.execute(request)
        room = cursor.fetchone()

        if room is None : return RoomResource.notfound

        cursor = RoomResource.db.cursor()
        request = f"""
            SELECT id_meuble_client
            FROM Meuble_client
            WHERE id_piece = {id}
        """
        cursor.execute(request)

        furnitures = filter(
            lambda f: type(f) is FurnitureResource,
            [FurnitureResource.get(f[0]) for f in cursor.fetchall()]
                            )
        
        return RoomResource(room[0], room[1], room[2], furnitures)
    
    @staticmethod
    #TODO: FILTER BY ADDRESS
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

    def delete(self):
        db = RoomResource.db
        cursor = db.cursor()

        request = f'DELETE FROM Piece WHERE id_piece = {self.id}'
        cursor.execute(request)
        db.commit()

        return self

    def update(self, data):
        db = RoomResource.db
        cursor = db.cursor()

        if 'name' in data:
            name = data['name'].replace("'", "\\'")
            request = f"""
                UPDATE Piece
                SET nom = '{name}'
                WHERE id_piece = {self.id}
            """
            cursor.execute(request)
        
        db.commit()
        return RoomResource.get(self.id)

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