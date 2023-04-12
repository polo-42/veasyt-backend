from db.BaseResource import BaseResource

class CatalogueResource(BaseResource):
    def __init__(self,id,name,weight,width,length,height,icon):
        self.id = id
        self.name = name
        self.weight = weight
        self.dimension = (width,length,height)
        self.icon = icon

    @staticmethod
    def get(id):
        return CatalogueResource.notallowed

    @staticmethod
    def getall(idcategory):
        cursor = CatalogueResource.db.cursor()
        request = f"""
            SELECT c.id_meuble_catalogue, nom_meuble, poids, largeur, longueur, hauteur, icone
            FROM Meuble_catalogue AS c, Meuble_categories AS d 
            WHERE d.id_meuble_catalogue = c.id_meuble_catalogue 
            AND d.id_categorie = {idcategory}
        """
        cursor.execute(request)
               
        return [
            CatalogueResource(c[0],c[1],c[2],c[3],c[4],c[5],c[6])
            for c in cursor.fetchall()
        ]
    
    def add(data):
        return CatalogueResource.notallowed
    
    def delete():
        return CatalogueResource.notallowed

class CategoryResource(BaseResource):

    def __init__(self,id,name,class_,catalogue):
        self.id = id
        self.name = name
        self.class_ = class_
        self.catalogue = catalogue

    @staticmethod
    def get(id):
        cursor = CategoryResource.db.cursor()
        request = f"""
            SELECT id_categorie, nom_categorie, classe
            FROM Meuble_categorie
            WHERE id_categorie = {id}
        """
        cursor.execute(request)
        c = cursor.fetchone()
        if c == None : return CategoryResource.notfound

        (idcat, name, class_) = (c[0], c[1], c[2])
        catalogue = CatalogueResource.getall(idcat)
        
        return CategoryResource(idcat,name,class_,catalogue)

    @staticmethod
    def getall(class_):
        cursor = CategoryResource.db.cursor()
        request = f"""
            SELECT id_categorie
            FROM Meuble_categorie
            WHERE classe = '{class_}'
        """
        cursor.execute(request)

        return [
            CategoryResource.get(c[0])
            for c in cursor.fetchall()
        ]

    @staticmethod   
    def add(data):
        return CategoryResource.notallowed
    
    def delete():
        return CategoryResource.notallowed

    def todict(self):
        return {
                "id" : self.id,
                "name" : self.name,
                "furnitures" : [ f.todict() for f in self.catalogue ]
            }