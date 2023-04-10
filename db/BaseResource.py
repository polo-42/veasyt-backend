from abc import ABC, abstractmethod, abstractstaticmethod
import mysql.connector

class BaseResource(ABC):

    notfound = 404
    notallowed = 405

    db = mysql.connector.connect(
            host="amenitydev-veasyt.mysql.database.azure.com",
            user="amenitydev",
            password="woYASh$7$B6g866w",
            database="veasyt_db"
        )
    
    @abstractstaticmethod
    def get(id):
        pass

    @abstractstaticmethod
    def getall():
        pass

    @abstractstaticmethod   
    def add(data):
        pass
    
    @abstractmethod
    def delete():
        pass

    def todict(self):
        return {
            k: v 
            for k, v in vars(self).items() 
            if v is not None
        }

    