from pydantic import BaseModel
from typing import List

class Teams(BaseModel):
    names : List[str] 


class Scraper(BaseModel):
    results : List[dict]


class users(BaseModel):
    username : str
    email:str