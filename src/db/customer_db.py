from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.models import Customer
from src.schemas.schemas import CustomerCreate, CustomerBase, AddressBase
from src.db.address_db import get_address_by_id


def get_customer_by_id(customer_id: int, db: Session):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_by_email(email: str, db: Session):
    return db.query(Customer).filter(Customer.email == email).first()

def get_customer_by_address_id(address_id: int, db: Session):
    return db.query(Customer).filter(Customer.address_id == address_id).first()

def get_all_customers(db: Session):
    return db.query(Customer).all()

def create_customer(customer: CustomerCreate, address_id: int, db:Session):
    customer_object = Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        address_id=address_id
    )

    db.add(customer_object)
    db.commit()
    db.refresh(customer_object)

    return customer_object
    
def delete_customer(customer_id: int, db: Session):
    customer_object = get_customer_by_id(customer_id, db=db)
    db.delete(customer_object)
    db.commit()

def update_customer(customer_id: int, customer: CustomerBase, db:Session):
    customer_object = get_customer_by_id(customer_id, db=db)

    for attribute in ["first_name", "last_name", "email"]:
        exec(f"setattr(customer_object, \"{attribute}\", customer.{attribute})")
    
    db.commit()
    db.refresh(customer_object)

    return customer_object
    
def update_customer_address(address_id: int, address: AddressBase, db:Session):
    address_object = get_address_by_id(address_id=address_id, db=db)

    for attribute in ["country", "city", "line_1", "line_2"]:
        exec(f"setattr(address_object, \"{attribute}\", address.{attribute})")
    
    db.commit()
    db.refresh(address_object)

    return address_object
