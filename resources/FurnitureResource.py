from resources.BaseResource import BaseResource
from resources.CatalogueResource import CatalogueResource   

class FurnitureResource(BaseResource):
    #TODO: mettre les DDL dans une transaction, regarder comment faire avec mysql.connector

    def __init__(self, id, quantity, id_catalogue, id_room, id_unload_address,custom_data=None):
        self.id = id
        self.quantity = quantity
        self.id_room = id_room
        self.id_unload_address = id_unload_address
        self.id_catalogue = id_catalogue

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
            if default[2] == None : return FurnitureResource.notfound
            return FurnitureResource(default[0],default[1],default[2],default[3],default[4])
        
        request = f"""
            SELECT poids, largeur, longueur, hauteur, emballage, deballage, demontage, remontage, infos_supplementaires
            FROM Meuble_avance
            WHERE id_meuble_client = {id}
        """
        cursor.execute(request)
        custom = cursor.fetchone()

        if custom is None : return FurnitureResource.notfound
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
        return filter(
            lambda f : type(f) is FurnitureResource,
            [ FurnitureResource.get(f[0]) for f in cursor.fetchall() ])
    
    @staticmethod
    def add(data):
        db = FurnitureResource.db
        cursor = db.cursor()
        custom = True if 'is_custom' in data and data['is_custom'] else False
        
        request = f"""
            INSERT INTO Meuble_client (est_avance, quantite, id_piece, id_adresse_dechargement)
            VALUES ({custom},{data['quantity']},{data['id_room']},{data['id_unload_address']})
            """
        cursor.execute(request)

        request = "SELECT LAST_INSERT_ID()"
        cursor.execute(request)
        id_furniture = cursor.fetchone()[0]

        if custom:
            add_info = data['additional_info'].replace("'", "\\'")
            request = f"""
            INSERT INTO Meuble_avance (id_meuble_client, poids, largeur, longueur, hauteur, emballage, deballage, remontage, demontage, infos_supplementaires, id_meuble_catalogue)
            VALUES ({id_furniture},{data['weight']},{data['width']},{data['length']},{data['height']},{data['packing']},{data['unpacking']},{data['disassembly']},{data['reassembly']}, '{add_info}',{data['id_catalogue']})
            """
        else:
            request = f"""
            INSERT INTO Meuble_client_defaut (id_meuble_client, id_meuble_catalogue)
            VALUES ({id_furniture}, {data['id_catalogue']})
            """

        cursor.execute(request)
        db.commit()
        return FurnitureResource.get(id_furniture)

    def delete(self):
        db = FurnitureResource.db
        cursor = db.cursor()

        if self.is_custom:
            request = f'DELETE FROM Meuble_avance WHERE id_meuble_client = {self.id}'
        else:
            request = f'DELETE FROM Meuble_client_defaut WHERE id_meuble_client = {self.id}'
        
        cursor.execute(request)

        request = f'DELETE FROM Meuble_client_defaut WHERE id_meuble_client = {self.id}'
        cursor.execute(request)

        db.commit()
        return self

    def update(self, data):
        #TODO: permettre de transformer un meuble defaut en avance -> (delete->add)
        db = FurnitureResource.db
        cursor = db.cursor()

        if 'quantity' in data : 
            cursor.execute(f"""
                UPDATE Meuble_client
                SET quantite = {data['quantity']}
                WHERE id_meuble_client = {self.id}
            """)
                
        db.commit()

        if not self.is_custom : return FurnitureResource.get(self.id)

        make_request = lambda set: f"""
                UPDATE Meuble_avance
                {set}
                WHERE id_meuble_client = {self.id}
            """

        update_attr = lambda attr, value: cursor.execute(make_request(f"SET {attr} = {value}")) 

        if 'weight' in data :
            update_attr('poids',data['weight'])
        if 'length' in data :
            update_attr('longueur',data['length'])
        if 'width' in data :
            update_attr('largeur',data['width'])
        if 'height' in data :
            update_attr('hauteur',data['height'])
        if 'packing' in data :
            print(data['packing'])
            update_attr('emballage',data['packing'])
        if 'unpacking' in data :
            update_attr('deballage',data['unpacking'])
        if 'disassembly' in data :
            update_attr('demontage',data['disassembly'])
        if 'reassembly' in data :
            update_attr('remontage',data['reassembly'])
        if 'additional_info' in data :
            add_info = data['additional_info'].replace("'", "\\'")
            update_attr('poids',f"'{add_info}'")
        
        db.commit()
        
        return FurnitureResource.get(self.id)


    def getvolume(self):
        return (self.dimension[0]*self.dimension[1]*self.dimension[2]/1000000)*self.quantity

    @staticmethod
    def istrue(mysqlbool):
        return True if mysqlbool != 0 else False