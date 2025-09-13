from fastapi import APIRouter
from module import Teams, Scraper,users
from database import (
    create_users,
    add_fav_teams,
    update_fav_teams,
    delete_fav,
    delete_all,
    find_fav,
)
router = APIRouter()


@router.post("/api/users")
async def create(user : users):
    respone = await create_users(user)
    return respone

@router.post("/api/users/{username}/teams")
async def addFav(user: str, teams: Teams):
     respone =await add_fav_teams(user,teams)
     if respone == 0:
         
        return {"error": "User not found"}

     return {"msg": "Teams added", "teams": teams.names}
@router.put("/api/users/{username}/teams/{index}")
async def updateFav(user:str, teams:str,index:int):
    response = await update_fav_teams(user, teams,index)
    if response == 0:
        return {"error": "User not found"}
    
    return {"msg": "Teams updated", "teams": teams}
@router.delete("/api/users/{username}/teams/{index}")
async def deleteFav(user:str,index:int):
    response = await delete_fav(user,index)
    if response == 0:
        return {"error": "User not found"}
    return {"msg": "Teams updated"}
@router.delete("/api/users/{username}/teams")
async def deleteAllFav(user:str):
    response = await delete_all(user)
    if response ==0:
        return  {"error": "User not found"}
    return {"msg":"teams deleted"}
@router.get("/api/users/{username}/teams")
async def findFav(user:str):
    respone = await find_fav(user)
    return respone
    
    