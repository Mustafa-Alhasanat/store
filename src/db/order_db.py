from fastapi import Depends
from sqlalchemy.orm import Session

from src.models.models import Order
from src.schemas.schemas import OrderCreate


def get_order_by_id(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_customer_orders(customer_id: int, db: Session):
    return db.query(Order).filter(Order.customer_id == customer_id).all()

def create_order(customer_id: int, order: OrderCreate, db: Session):
    order_object = Order(
        payment_method=order.payment_method, 
        brand=order.brand,
        state=order.state,
        customer_id=customer_id
    )
    
    db.add(order_object)
    db.commit()
    db.refresh(order_object)

    return order_object

def delete_order(order_id: int, db: Session):
    order_object = get_order_by_id(order_id, db=db)
    db.delete(order_object)
    db.commit()

def delete_orders_by_customer_id(customer_id: int, db: Session):
    db.query(Order).filter(Order.customer_id == customer_id).delete()
    db.commit()
