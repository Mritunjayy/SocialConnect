from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from .config import settings

from psycopg2.extras import RealDictCursor##so psycopg2 dosent pass the column header/name when any query is asked , it just gives the rows , so for header also, we use this....


## removing this afterwards since anyone can see this once uploaded on 
# print("kaalu",settings)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# postgresql://postgres_fastapi:fmbavs78D5C0xULZkPpz3ONhGuw4e9dY@dpg-cqektq0gph6c73art5dg-a.oregon-postgres.render.com/fastapi_60p6

engine= create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)

Base= declarative_base()

#dependency for this orm
def get_db():
    db = SessionLocal()##responsible for talking with databases..
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn= psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='root123', cursor_factory=RealDictCursor)
#         cursor= conn.cursor()
#         print("Database connection established")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)