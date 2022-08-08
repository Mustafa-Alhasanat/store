from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from src.schemas.schemas import CustomerSchema, CustomerBase, CustomerCreate, AddressBase, AddressSchema
from src.models.models import Customer, Address
from src.db.database import SessionLocal, engine, get_db
from src.db.customer_db import get_customer_by_id, get_all_customers, get_customer_by_email, create_customer, update_customer, update_customer_address, delete_customer
from src.db.address_db import get_address_by_id, get_all_addresses, create_address, delete_address
from src.db.order_db import delete_orders_by_customer_id


customer_router = APIRouter()


@customer_router.get("/{customer_id}", response_model=CustomerSchema, tags=["customers"], status_code=200)
def get_customer_object(customer_id: int, response: Response, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail="Customer not found")
    
    response.status_code = status.HTTP_200_OK
    return customer_object
    

@customer_router.get("/address/{customer_id}", response_model=AddressSchema, tags=["customers"], status_code=200)
def get_customer_address_object(customer_id: int, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    address_obj = get_address_by_id(address_id=customer_object.address_id, db=db) 

    return address_obj


@customer_router.get("/all/", tags=["customers"], response_model=list[CustomerSchema])
def get_customers_object(db: Session = Depends(get_db)):
    all_customers = get_all_customers(db=db)

    if all_customers is None:
        raise HTTPException(status_code=404, detail="Customers list is empty")
    
    return all_customers


# --------------------------------

@customer_router.post("/", tags=["customers"], response_model=CustomerSchema, status_code=201)
def create_customer_object(customer: CustomerCreate, db: Session = Depends(get_db)):
    customer_obj = get_customer_by_email(email=customer.email, db=db)

    if customer_obj is not None:
        raise HTTPException(status_code=400, detail="Customer already registered")

    address_object = create_address(address=customer.address, db=db)

    customer_object = create_customer(customer=customer, address_id=address_object.id, db=db)

    return customer_object
    
# --------------------------------

@customer_router.delete("/{customer_id}", response_model=dict, tags=["customers"], status_code=200)
def delete_customer_object(customer_id: int, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    address_id = customer_object.address_id

    delete_orders_by_customer_id(customer_id=customer_id, db=db)
    delete_customer(customer_id=customer_id, db=db)
    delete_address(address_id=address_id, db=db)

    return {"message": f"Customer {customer_id} have been deleted along with their address and orders"}

# --------------------------------

@customer_router.put("/{customer_id}", response_model=CustomerSchema, tags=["customers"], status_code=202)
def update_customer_object(customer_id: int, customer: CustomerBase, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    new_customer = update_customer(customer_id=customer_id, customer=customer, db=db)

    return new_customer


@customer_router.put("/address/{customer_id}", response_model=AddressSchema, tags=["customers"], status_code=202)
def update_customer_address_object(customer_id: int, address: AddressBase, db: Session = Depends(get_db)):
    customer_object = get_customer_by_id(customer_id=customer_id, db=db)
    
    if customer_object is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    address_object = get_address_by_id(customer_object.address_id, db=db)

    if address_object is None:
        raise HTTPException(status_code=404, detail="Address not found")

    new_address = update_customer_address(address_id=address_object.id, address=address, db=db)

    return new_address  


