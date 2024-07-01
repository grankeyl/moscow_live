from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database.db_connect import create_tables
from database.managers import User

app = FastAPI()

templates = Jinja2Templates(directory="./templates")

app.mount("/static", StaticFiles(directory="./static"), name="static")

if __name__ == "__main__":
    import uvicorn, asyncio
    
    from routes.routes import *

    asyncio.run(create_tables())
    uvicorn.run(app, host="127.0.0.1", port=5000)
