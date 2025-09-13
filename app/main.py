from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from .db.connection import connect_to_mongo, close_mongo_connection
from .api.timetable import router as timetable_router
from .api.groups import router as groups_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await connect_to_mongo()
#     yield
#     await close_mongo_connection()

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(timetable_router, prefix="/api", tags=["Timetables"])
app.include_router(groups_router, prefix="/api", tags=["Groups"])
