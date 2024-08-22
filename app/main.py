from contextlib import asynccontextmanager

from app.database import close_db, init_db
from app.router import router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
