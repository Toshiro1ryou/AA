from fastapi import FastAPI,HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from routers import user_db,scrap
from module import  Teams,Scraper,users




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



app.include_router(user_db.router)
app.include_router(scrap.router)

    



