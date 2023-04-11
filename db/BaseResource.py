from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any
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
    def get(id: int) -> object|int:
        pass

    @abstractstaticmethod
    def getall() -> list[object]:
        pass

    @abstractstaticmethod   
    def add(data: dict[str,Any]) -> object|int:
        pass
    
    @abstractmethod
    def delete() -> object|int:
        pass

    def todict(self) -> dict[str,Any]:
        return {
            k: v 
            for k, v in vars(self).items() 
            if v is not None
        }

    