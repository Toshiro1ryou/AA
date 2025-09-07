from pydantic import BaseModel
from typing import List

class FavTeams(BaseModel):
    teams : str
