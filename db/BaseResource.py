from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any
import mysql.connector

class BaseResource():

    badrequest = 400
    unauthorized = 401
    forbidden = 403
    notfound = 404
    notallowed = 405
    notacceptable = 406

    db = mysql.connector.connect(
            host="amenitydev-veasyt.mysql.database.azure.com",
            user="amenitydev",
            password="woYASh$7$B6g866w",
            database="veasyt_db"
        )
    
    def get(id: int) -> object|int:
        return BaseResource.notallowed

    def getall() -> list[object]:
        return BaseResource.notallowed
  
    def add(data: dict[str,Any]) -> object|int:
        return BaseResource.notallowed
    
    def delete() -> object|int:
        return BaseResource.notallowed
    
    def update(self, data) -> object|int:
        return BaseResource.notallowed

    def todict(self) -> dict[str,Any]:
        return {
            k: v 
            for k, v in vars(self).items() 
            if v is not None
        }
