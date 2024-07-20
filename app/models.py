from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.ext.declarative import declarative_base


# Base= declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id= Column(Integer, primary_key= True, nullable= False)
    title= Column(String, nullable= False)
    content= Column(String, nullable= False)
    published= Column(Boolean, server_default= "True")
    created_at= Column(TIMESTAMP(timezone=True), nullable= False, server_default= text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    ## it didn't add this column , since sqlalchemy first checks if there is any table present , if there is , it dosen't change anything , however, it does change if no table is present named posts
    ##so we use database migration tool, but for now we will do it manually...by dropping our post table..
    owner = relationship("User")
   

class User(Base):
    __tablename__ = "users"
    
    id= Column(Integer, primary_key= True, nullable= False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable= False, server_default= text('now()'))
    


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  

