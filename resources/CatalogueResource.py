from resources.BaseResource import BaseResource

class CatalogueResource(BaseResource):
    def __init__(self,id,name,weight,width,length,height,icon):
        self.id = id
        self.name = name
        self.weight = weight
        self.width = width
        self.length = length 
        self.height = height
        self.icon = icon

    @staticmethod 
    def get(id_furniture):
        cursor = CatalogueResource.db.cursor()
        request = f"""
        SELECT id_meuble_catalogue, nom_meuble, poids, largeur, longueur, hauteur, icone
        FROM Meuble_catalogue
        WHERE id_meuble_catalogue = {id_furniture}
        """
        cursor.execute(request)
        furniture = cursor.fetchone()
        if furniture == None : return CatalogueResource.notfound

        return CatalogueResource(furniture[0],furniture[1],furniture[2],furniture[3],furniture[4],furniture[5],furniture[6])

    @staticmethod #OK
    def getall(id_category):
        cursor = CatalogueResource.db.cursor()
        request = f"""
           SELECT catalogue.id_meuble_catalogue, nom_meuble, poids, largeur, longueur, hauteur, icone
           FROM Meuble_catalogue AS catalogue, Meuble_categories AS categories 
            WHERE categories.id_meuble_catalogue = catalogue.id_meuble_catalogue 
            AND categories.id_categorie = {id_category}
        """
        cursor.execute(request)
        furnitures = cursor.fetchall()
        if furnitures == None : return CatalogueResource.notfound
        return [
            CatalogueResource(furniture[0],furniture[1],furniture[2],furniture[3],furniture[4],furniture[5],furniture[6])
            for furniture in furnitures
        ]
    
    @staticmethod
    def add(data):
        cursor = CatalogueResource.db.cursor()
        request = f"""
        INSERT INTO Meuble_catalogue (nom_meuble, poids, largeur, longueur, hauteur, icone)
        VALUES ('{data["name"]}',{data["weight"]},{data["width"]},{data["length"]},{data["height"]},'{data["icon"]}')
        """
        cursor.execute(request)
        CatalogueResource.db.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')      
        id_furniture = cursor.fetchone()[0]
        id_category = data["id_category"]
    
        request = f"""
        INSERT INTO Meuble_categories (id_meuble_catalogue, id_categorie)
        VALUES ({id_furniture}, {id_category})
        """

        cursor.execute(request)
        CatalogueResource.db.commit()

        return CatalogueResource.get(id_furniture)
        
    def delete():
        #TODO: Restrict deletion on default furnitures
        return CatalogueResource.notallowed
    

    def update(self, data): 
        cursor = CatalogueResource.db.cursor()
        if "name" in data :
            request = f"""
            UPDATE Meuble_catalogue
            SET nom_meuble = '{data["name"]}'
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()        
        
        if "weight" in data:
            request = f"""
            UPDATE Meuble_catalogue
            SET poids = {data["weight"]}
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()

        if 'width' in data:
            request = f"""
            UPDATE Meuble_catalogue
            SET largeur = {data["width"]}
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()

        if 'length' in data:
            request = f"""
            UPDATE Meuble_catalogue
            SET longueur = {data["length"]}
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()

        if "height" in data:
            request = f"""
            UPDATE Meuble_catalogue
            SET hauteur = {data["height"]}
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()

        if "icon" in data:
            request = f"""
            UPDATE Meuble_catalogue
            SET icone = '{data["icon"]}'
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()

        if "id_category" in data:
            request = f"""
            UPDATE Meuble_categories
            SET id_categorie = {data["id_category"]}
            WHERE id_meuble_catalogue = {self.id}
            """
            cursor.execute(request)
            CatalogueResource.db.commit()        

        return CatalogueResource.get(self.id)

class CategoryResource(BaseResource):
    def __init__(self,id,name,class_,catalogue):
        self.id = id
        self.name = name
        self.class_ = class_
        self.catalogue = catalogue

    @staticmethod
    def get(id_category):
        cursor = CategoryResource.db.cursor()
        request = f"""
        SELECT id_categorie, nom_categorie, classe
        FROM Meuble_categorie
        WHERE id_categorie = {id_category}
        """
        cursor.execute(request)
        category = cursor.fetchone()
        if category == None : return CategoryResource.notfound

        (id_category, name, class_) = (category[0], category[1], category[2])
        catalogue = CatalogueResource.getall(id_category)
        
        return CategoryResource(id_category,name,class_,catalogue)

    @staticmethod
    def getall(class_):
        cursor = CategoryResource.db.cursor()
        request = f"""
        SELECT id_categorie
        FROM Meuble_categorie
        WHERE classe = '{class_}'
        """
        cursor.execute(request)
        categories = cursor.fetchall()

        return [
            CategoryResource.get(category[0])
            for category in categories
        ]

    @staticmethod   
    def add(data):
        cursor = CategoryResource.db.cursor()
        request = f"""
        INSERT INTO Meuble_categorie (nom_categorie, classe)
        VALUES ('{data["name"]}','{data["class"]}')
        """
        cursor.execute(request)
        CategoryResource.db.commit()

        cursor.execute('SELECT LAST_INSERT_ID()')      
        id_category = cursor.fetchone()[0]
        return CategoryResource.get(id_category)
    
    def delete():
        #TODO: Restrict deletion on default categories
        return CategoryResource.notallowed
    

    def update(self, data): 
        cursor = CategoryResource.db.cursor()
        if 'name' in data :
            request = f"""
            UPDATE Meuble_categorie
            SET nom_categorie = '{data["name"]}'
            WHERE id_categorie = {self.id}
            """
        cursor.execute(request)
        CategoryResource.db.commit()

        if 'class' in data :
            request = f"""
            UPDATE Meuble_categorie
            SET classe = '{data["class"]}'
            WHERE id_categorie = {self.id}
            """
        cursor.execute(request)
        CategoryResource.db.commit()  

        return CategoryResource.get(self.id)

    def todict(self):
        return {
                "id" : self.id,
                "name" : self.name,
                "furnitures" : [ 
                    f.todict() for f in self.catalogue 
                    if type(f) is CatalogueResource
                    ]
            }