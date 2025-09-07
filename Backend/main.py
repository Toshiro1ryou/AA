from fastapi import FastAPI,HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from module import FavTeams
from database import (
    fetch_Favteams,
    choose_Favteams, 
    update_Favteams,
    remove_Favteams,
)



app = FastAPI()
@app.get("/")
def home():

    return{"home":"here"}


origins= [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    )
@app.get("/api/favTeams")
async def get_favTeams():
    response = await fetch_Favteams()
    return response


@app.post("/api/favTeams", response_model = FavTeams)
async def Post_favTeams(teams):
    print("hello")
    response = await choose_Favteams(teams)
    if not response:
        raise HTTPException(404,"Somenthing went wrong")
    return response


@app.put("/api/favTeams")
async def put_favTeams(teams):
    response = await update_Favteams(teams)
    if not response:
        raise HTTPException(404,"Somenthing went wrong")
    return response

@app.delete("/api/favTeams")
async def delete_favTeams(teams):
    response  = await remove_Favteams(teams)
    if not response:
        raise HTTPException(404,"Somenthing went wrong")
    return response