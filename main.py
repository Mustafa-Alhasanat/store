from fastapi import FastAPI

from src.models import models
from src.schemas import schemas
from src.db.database import engine, Base
from src.controllers.customer import router as customer_router
from src.controllers.address import router as address_router
from src.controllers.order import router as order_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(address_router, prefix="/address")
app.include_router(order_router, prefix="/order")