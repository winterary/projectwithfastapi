from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings


# from typing import List
# from fastapi import FastAPI, Response, status, HTTPException, Depends, Path
# from pydantic import BaseModel
# from random import randrange
# import psycopg
# from psycopg.rows import dict_row
# import time
# from . import models, schemas, utils
# from .database import engine, SessionLocal, get_db
# from sqlalchemy.orm import Session
# from sqlalchemy import select
# from .routers import posts, users, auth

def get_database_url(testing: bool = False) -> str:
    suffix = "_test" if testing else ""
    return(
        f"postgresql+psycopg://{settings.database_username}:"
        f"{settings.database_password}@{settings.database_hostname}:"
        f"{settings.database_port}/{settings.database_name}{suffix}"
    )

SQLALCHEMY_DATABASE_URL = get_database_url()

# postgresql+psycopg://postgres:f4ngyuan@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres',
#                         password = 'f4ngyuan', row_factory = dict_row )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
