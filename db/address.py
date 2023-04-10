import mysql.connector
from db.base import baseModel

mydb = mysql.connector.connect(
    host="amenitydev-veasyt.mysql.database.azure.com",
    user="amenitydev",
    password="woYASh$7$B6g866w",
    database="veasyt_db"
)

cursor = mydb.cursor(buffered=True)

class Address_postal(baseModel):
    def __init__(self,id,street,number,region,city,country): #TODO: define optionnal fields
        self.id = id
        self.street = street
        self.number = number
        self.region = region
        self.city = city   
        self.country = country

    @staticmethod
    def fromjson(data):
        """init from json data"""
        address = Address_postal(None, data['street'], data['number'], data['region'], data['city'], data['country'])
        return address

    def save(self):
        request = (f"""
            INSERT INTO Adresse_postale (rue, numero, localite, ville, pays) 
            VALUES ('{self.street}',{self.number},'{self.region}','{self.city}','{self.country}');
            """)
        cursor.execute(request)
        mydb.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')
        return cursor.fetchone()[0]

    def todict(self):
        return {k: v for k, v in vars(self).items() if v is not None}

    @staticmethod
    def getAll(filter=None):
        pass 

class Address(Address_postal):
    def __init__(self,id,street,number,region,city,country,date_start,date_end,is_loading,floor,usable_lift,freight_lifter,parking_distance,additional_info,id_visit,id_address_postal):
            super().__init__(id,street,number,region,city,country)
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

    pass

class Address_unload(Address):
    pass
    
class Address_load(Address):
    pass
