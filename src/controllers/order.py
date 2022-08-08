from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas.schemas import OrderCreate, OrderSchema
from src.db.database import SessionLocal, engine, get_db
from src.db.order_db import get_order_by_id, get_all_orders, get_customer_orders, create_order, delete_order, delete_orders_by_customer_id
from src.db.customer_db import get_customer_by_id


order_router = APIRouter()


@order_router.get("/{order_id}", response_model=OrderSchema, tags=["orders"], status_code=200)
def get_order_object(order_id: int, db: Session = Depends(get_db)):
    order_object = get_order_by_id(order_id=order_id, db=db)
    
    if order_object is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order_object


@order_router.get("/all/", response_model=list[OrderSchema], tags=["orders"], status_code=200)
def get_order_objects(db: Session = Depends(get_db)):
    all_orders = get_all_orders(db=db)

    if all_orders is None:
        raise HTTPException(status_code=404, detail="Orders list is empty")
    
    return all_orders


@order_router.get("/customer/{customer_id}", response_model=list[OrderSchema], tags=["orders"], status_code=200)
def get_order_objects(customer_id: int, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer_orders = get_customer_orders(customer_id=customer_id, db=db)

    if customer_orders is None:
        raise HTTPException(status_code=404, detail="Orders list is empty")
    
    return customer_orders

# --------------------------------

@order_router.post("/{customer_id}", tags=["orders"], response_model=OrderSchema, status_code=201)
def create_order_object(customer_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    order_object = create_order(customer_id=customer_id, order=order, db=db)

    return order_object
    
# --------------------------------

@order_router.delete("/{order_id}", response_model=dict, tags=["orders"], status_code=200)
def delete_order_object(order_id: int, db: Session = Depends(get_db)):
    order_object = get_order_by_id(order_id=order_id, db=db)
    
    if order_object is None:
        raise HTTPException(status_code=404, detail="Order not found")

    delete_order(order_id=order_id, db=db)

    return {"message": f"Order {order_id} has been deleted"}


@order_router.delete("/customer/{customer_id}", response_model=dict, tags=["orders"], status_code=200)
def delete_orders_by_customer_id_object(customer_id: int, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_orders = get_customer_orders(customer_id=customer_id, db=db)

    if customer_orders is None:
        raise HTTPException(status_code=404, detail="Orders list is empty")

    delete_orders_by_customer_id(customer_id=customer_id, db=db)

    return {"message": f"Orders for customer {customer_id} have been deleted"}
