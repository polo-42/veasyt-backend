from resources.BaseResource import BaseResource

class AddressResource(BaseResource):
    def __init__(self,id,date_start,date_end,is_loading,floor,usable_lift,freight_lifter,parking_distance,additional_info,id_visit,id_address_postal,street,number,region,city,country): #TODO: define optionnal fields
        self.id = id
        self.date_start = date_start
        self.date_end = date_end
        self.is_loading = is_loading
        self.floor = floor
        self.usable_lift = usable_lift
        self.freight_lifter = freight_lifter
        self.parking_distance = parking_distance
        self.additional_info = additional_info
        self.id_visit = id_visit
        self.id_address_postal = id_address_postal
        self.street = street
        self.number = number
        self.region = region
        self.city = city   
        self.country = country

    def get(id_address):
        cursor = AddressResource.db.cursor()
        request = f"""
        SELECT adr.id_adresse, adr.date_depuis, adr.date_jusqua, adr.is_chargement, adr.etage_logement, adr.ascenseur_utilisable, adr.monte_meuble, adr.distance_parking, adr.info_supplementaire, adr.id_visite, adr.id_adresse_postale, postal.rue,postal.numero,postal.localite,postal.ville,postal.pays
        FROM Adresse AS adr, Adresse_postale AS postal
        WHERE adr.id_adresse = {id_address}
        AND adr.id_adresse_postale = postal.id_adresse_postale
        """
        cursor.execute(request)
        address = cursor.fetchone()
        if address == None : return AddressResource.notfound
        return AddressResource(address[0],address[1],address[2],address[3],address[4],address[5],address[6],address[7],address[8],address[9],address[10],address[11],address[12],address[13],address[14],address[15])

    def getall(id_visit):
        cursor = AddressResource.db.cursor()
        request = f"""
        SELECT id_adresse
        FROM Adresse
        WHERE id_visite = {id_visit}
        """
        cursor.execute(request)
        addresses = cursor.fetchall()
        if addresses == None : return AddressResource.notfound
        return filter(
            lambda f : type(f) is AddressResource,
            [AddressResource.get(f[0]) for f in addresses])
  
    def add(data):
        cursor = AddressResource.db.cursor()
        request = (f"""
        INSERT INTO Adresse_postale (rue, numero, localite, ville, pays) 
        VALUES ('{data["street"]}',{data["number"]},'{data["region"]}','{data["city"]}','{data["country"]}')
        """)
        cursor.execute(request)
        AddressResource.db.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        id_address = cursor.fetchone()[0]
        return AddressResource(id_address,data["street"],data["number"],data["region"],data["city"],data["country"])
    
    def delete(id_address):
        return AddressResource.notallowed
        cursor = AddressResource.db.cursor()

        request = (f"""
        SELECT 
        WHERE id_adresse_postale = {id_address}
        """)

        request = (f"""
        DELETE FROM Adresse
        WHERE id_adresse_postale = {id_address}
        """)
        cursor.execute(request)
        AddressResource.db.commit()

        request = (f"""
        DELETE FROM Adresse_postale
        WHERE id_adresse_postale = {id_address}
        """)
        cursor.execute(request)
        AddressResource.db.commit()
        return 200
         
    def update(self, data):
        return AddressResource.notallowed
        

    #def todict(self):
        return {
                "id" : self.id,
                "date_start" : self.date_start,
                "date_end" : self.date_end,
                "is_loading" : self.is_loading,
                "floor" : self.floor,
                "usable_lift" : self.usable_lift,
                "freight_lifter" : self.freight_lifter,
                "parking_distance" : self.parking_distance,
                "additional_info" : self.additional_info,
                "id_visit" : self.id_visit,
                "id_address_postal" : self.id_address_postal,
                "street" : self.street,
                "number" : self.number,
                "region" : self.region,
                "country" : self.country  
            }
