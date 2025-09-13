from fastapi import APIRouter
from app import root
from database import(
    insert_matches,
    email,

)

from module import  Teams,Scraper,users

router = APIRouter()


@router.get("/api/scrap")
async def scraper():
    response = await root()
    result = await insert_matches(response)
    return result




@router.post("/api/email-sender")
async def emailSender(user:str):

    response = await email(user)
    return response

