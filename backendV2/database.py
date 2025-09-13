from module import Teams , Scraper,users
import motor.motor_asyncio 
from typing import List
from emailSetting import send_email

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.Fav_teams
scrap_collection = database.scrap
user_collection = database.users


    
async def create_users(user:users):
    document = await user_collection.find_one({"username":user.username})
    if document :
        return {"error": "User with that name alr exist"}
    
    await user_collection.insert_one(user.dict())
    return {"msg": "User created"}






async def get_user(username: str):
    user = await user_collection.find_one({"username": username})
    return user



async def add_fav_teams(user: str, teams: Teams):
    result = await user_collection.update_one(
        {"username": user}, 
        {"$addToSet": {"fav_teams": {"$each": teams.names}}}
    )

    respone =  result.matched_count
    return respone

async def update_fav_teams(user:str, teams:str,index:int):
    field = f"fav_teams.{index}"
    result = await user_collection.update_one(
        {"username": user},
        {"$set": {field: teams}}
    )
    response = result.matched_count
    return response

async def delete_fav(user:str,index:int):
    field = f"fav_teams.{index}"
    await user_collection.update_one(
        {"username": user},
        {"$unset": {field: 1}}
    )
    result = await user_collection.update_one(
        {"username": user},
        {"$pull": {"fav_teams": None}}
    )
    response = result.matched_count
    return response

async def delete_all(user:str):
    result = await user_collection.update_one(
        {"username": user},
        {"$unset": {"fav_teams": ""}} 
    )
    response = result.matched_count
    return response
        

async def find_fav(user:str):
    results = await user_collection.find({"username":user}).to_list(length= None)
    for result in results:
        if "_id" in result:
            result["_id"] = str(result["_id"])
    return results

    
async def insert_matches(matches: list[dict]):
    for match in matches:
        exists = await scrap_collection.find_one({
            "league": match["league"],
            "team1": match["team1"],
            "team2": match["team2"],
            "date": match["date"],
        })
        if not exists:
            await scrap_collection.insert_one(match)
           
    return {"msg":"done"}


async def email(user:str):
    db_user = await user_collection.find_one({"username": user})
    
    if not db_user:
        return {"msg":"user not found"}

    
    email = db_user["email"]

    send_email(
        subject="TEst",
        body=f"Hi {user}, this is a test email.",
        to_email=email
    )

    return {"msg": f"Email sent to {email}"}
    

