"""some things to know: a) usrs send a request to the fast api with some features/ attributes that an be made as different as designed, like user can send me str instead of int required, so this requires a schema model for request;
b) now response schema is also required , like if we are working with any bank database or any ther confidential things database, then user would send password with the request but dont the password back as a response since he knows his password so it becomes imp to set response schemas """


from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool= True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


## this schema makes sure the request coming from the client is in this fromat.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool= True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes=True

#-------------------
# class OwnerEmail(BaseModel):
#     email: EmailStr

#     class Config:
#         orm_mode = True
#-------------------


## now we create another schema/pydantic model for the request being sent to user/client
class PostResponse(BaseModel):
# class PostResponse(PostBase):

## we also need to add owner_id since user need to see who created the post, so lets update this response schema
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut
    # votes: int
    # owner: OwnerEmail
     
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: PostResponse
    Votes: int

    class Config:
        from_attributes=True



class UserCreate(BaseModel):
    email: EmailStr 
    password: str



# class PostUpdate(PostBase):


class UserLogin(BaseModel):
    email: EmailStr
    password: str

##defining schema for the token
class Token(BaseModel):
    access_token: str
    token_type: str

##also setting schema for the token data
class TokenData(BaseModel):
    id: Optional[int]= None


#---------------------------
class Vote(BaseModel):
    post_id: int
    dir: conint (le=1)

