# from fastapi.params import Body 
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange
# from  sqlalchemy.orm import Session
from fastapi import FastAPI
from app import models
from app.database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind = engine)

app= FastAPI()

# origins =["https://www.google.com", "https://www.youtube.com"] 
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"],
)

#3> now we want to save the posts to the database,cause now we are just sending the post to user.(working with databases , automatically creates an id for each information , but here we r not using database , so we ceate an id for each post)

# my_posts= [{"title": "title of post 1","content": "content of post 1", "id":1},{"title":"favourite foods","content":"i like pizza","id":2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"]==id:
#             return p
        


app.include_router(post.router)  
app.include_router(user.router)  
app.include_router(auth.router)  
app.include_router(vote.router)    
 
# @app.get("/login")
@app.get("/")
async def root():
    return {"message": "welcome to my world!!!!"} 


#7>> working postgres with python......> library: Psycopg




    