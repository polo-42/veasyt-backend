from db.BaseResource import BaseResource

class FurnitureResource(BaseResource):

    def __init__(self,id,quantity,id_catalogue,id_room,id_unload_address):
        self.id = id
        self.quantity = quantity
        self.id_catalogue = id_catalogue
        self.id_room = id_room
        self.id_unload_address = id_unload_address

    @staticmethod
    def get(id):
        cursor = FurnitureResource.db.cursor()
        cursor.execute(f"""
            SELECT nom_meuble, poids, largeur, longueur, hauteur, icone 
            FROM Meuble_catalogue
            WHERE id_meuble_catalogue = {id}
        """)

    @staticmethod
    def getall():
        pass

    @staticmethod   
    def add(data):
        pass
  
    def delete():
        pass

    def update(self, data):
        pass
    
    def getvolume(self):
        return (self.dimension[0]*self.dimension[1]*self.dimension[2]/1000000)*self.quantity
    