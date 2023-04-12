from db.BaseResource import BaseResource
from db.CatalogueResource import CatalogueResource   

class FurnitureResource(BaseResource):

    def __init__(self, id, quantity, id_catalogue, id_room, id_unload_address,custom_data=None):
        self.id = id
        self.quantity = quantity
        self.id_room = id_room
        self.id_unload_address = id_unload_address

        if custom_data == None:
            catalogue_furniture = CatalogueResource.get(id_catalogue) 
            self.weight = catalogue_furniture.weight
            self.length = catalogue_furniture.length
            self.height = catalogue_furniture.height
            self.width = catalogue_furniture.width
            self.is_custom = False
            self.packing = False
            self.unpacking = False
            self.disassembly = False
            self.reassembly = False
            self.additional_info = 'No additionnal information'
        
        else:
            self.weight = custom_data['weight']
            self.length = custom_data['length']
            self.height = custom_data['height']
            self.width = custom_data['width']
            self.is_custom = True
            self.packing = FurnitureResource.istrue(custom_data['packing'])
            self.unpacking = FurnitureResource.istrue(custom_data['unpacking'])
            self.disassembly = FurnitureResource.istrue(custom_data['disassembly'])
            self.reassembly = FurnitureResource.istrue(custom_data['reassembly'])
            self.additional_info = custom_data['additional_info']
        

    @staticmethod
    def get(id):
        cursor = FurnitureResource.db.cursor()
        request = f"""
            SELECT c.id_meuble_client, quantite, d.id_meuble_catalogue, id_piece, id_adresse_dechargement, est_avance
            FROM Meuble_client as c
            LEFT JOIN Meuble_client_defaut as d
            ON c.id_meuble_client = d.id_meuble_client
            WHERE c.id_meuble_client = {id}
        """
        cursor.execute(request)
        default = cursor.fetchone()
        if default == None : return FurnitureResource.notfound

        custom = default[5]
        if custom == 0:
            return FurnitureResource(default[0],default[1],default[2],default[3],default[4])
        
        request = f"""
            SELECT poids, largeur, longueur, hauteur, emballage, deballage, demontage, remontage, infos_supplementaires
            FROM Meuble_avance
            WHERE id_meuble_client = {id}
        """
        cursor.execute(request)
        custom = cursor.fetchone()
        custom_data = {
            'weight': custom[0],
            'width': custom[1],
            'length': custom[2],
            'height': custom[3],
            'packing': custom[4],
            'unpacking': custom[5],
            'disassembly': custom[6],
            'reassembly': custom[7],
            'additional_info': custom[8]
        }

        return FurnitureResource(default[0],default[1],default[2],default[3],default[4],custom_data)
    
    @staticmethod
    def getall(id_room):
        cursor = FurnitureResource.db.cursor()
        request = f"""
            SELECT id_meuble_client
            FROM Meuble_client
            WHERE id_piece = {id_room}
        """
        cursor.execute(request)
        return [
            FurnitureResource.get(f[0])
            for f in cursor.fetchall()
        ]



    def getvolume(self):
        return (self.dimension[0]*self.dimension[1]*self.dimension[2]/1000000)*self.quantity

    @staticmethod
    def istrue(mysqlbool):
        return True if mysqlbool != 0 else False