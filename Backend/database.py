from module import FavTeams
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.Fav_teams
collection = database.teams


async def fetch_Favteams(teams):
    document = await collection.find_one({"Teams":teams})
    return document

async def choose_Favteams(FavTeams):
    document = FavTeams
    result = await collection.insert_one({document})
    return result

async def update_Favteams(teams):
    await collection.update_one({"Teams" : teams})
    document = await collection.find_one({"Teams":teams})
    return document
async def remove_Favteams(teams):
    await collection.delete_one({"Teams":teams})
    return True
    