from resources.BaseResource import BaseResource

class VisitResource(BaseResource):

    def __init__(self, id, date, id_client):
        self.id = id
        self.date = date
        self.id_client = id_client

    @staticmethod
    def getall():
        cursor = VisitResource.db.cursor()
        request = f"""
            SELECT id_visite, date, id_client
            FROM Visite
        """
        cursor.execute(request)

        return [
            VisitResource(v[0],v[1],v[2])
            for v in cursor.fetchall()
        ]