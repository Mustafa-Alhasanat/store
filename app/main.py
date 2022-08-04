from fastapi import FastAPI

from app.src.models import models
from app.src.schemas import schemas
from app.src.db.database import engine, Base
# from app.src.controllers.customer import router as customer_router
# from app.src.controllers.address import router as address_router
# from app.src.controllers.order import router as order_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(users_router, prefix="/users")
# app.include_router(address_router, prefix="/address")
# app.include_router(order_router, prefix="/order")