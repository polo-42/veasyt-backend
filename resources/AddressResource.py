from resources.BaseResource import BaseResource

class AddressPostalResource(BaseResource):
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
        cursor = AddressPostalResource.db.cursor()
        request = f"""
        SELECT id_adresse_postale,rue,numero,localite,ville,pays
        FROM Adresse_postale
        WHERE id_adresse_postale = {id_address}
        """
        cursor.execute(request)
        address = cursor.fetchone()
        if address == None : return AddressPostalResource.notfound

        return AddressPostalResource(address[0],address[1],address[2],address[3],address[4],address[5],address[6])

    def getall():
        return AddressPostalResource.notallowed
  
    def add(data):
        cursor = AddressPostalResource.db.cursor()
        request = (f"""
        INSERT INTO Adresse_postale (rue, numero, localite, ville, pays) 
        VALUES ('{data["street"]}',{data["number"]},'{data["region"]}','{data["city"]}','{data["country"]}')
        """)
        cursor.execute(request)
        AddressPostalResource.db.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        id_address = cursor.fetchone()[0]
        return AddressPostalResource(id_address,data["street"],data["number"],data["region"],data["city"],data["country"])
    
    def delete(id_address):
        cursor = AddressPostalResource.db.cursor()

        request = (f"""
        SELECT 
        WHERE id_adresse_postale = {id_address}
        """)

        request = (f"""
        DELETE FROM Adresse
        WHERE id_adresse_postale = {id_address}
        """)
        cursor.execute(request)
        AddressPostalResource.db.commit()

        request = (f"""
        DELETE FROM Adresse_postale
        WHERE id_adresse_postale = {id_address}
        """)
        cursor.execute(request)
        AddressPostalResource.db.commit()
        return 200
         
    def update(self, data):
        pass