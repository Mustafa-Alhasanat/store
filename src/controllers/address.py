from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas.schemas import AddressSchema, AddressBase
from src.models.models import Address, Customer
from src.db.database import SessionLocal, engine, get_db
from src.db.address_db import get_address_by_id, get_all_addresses, delete_address
from src.db.customer_db import get_customer_by_address_id


address_router = APIRouter()


@address_router.get("/{address_id}", response_model=AddressSchema, tags=["addresses"], status_code=200)
def get_address_object(address_id: int, db: Session = Depends(get_db)):
    address_object = get_address_by_id(address_id=address_id, db=db)
    
    if address_object is None:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return address_object


@address_router.get("/all/", response_model=list[AddressSchema], tags=["addresses"], status_code=200)
def get_address_objects(db: Session = Depends(get_db)):
    all_addresses = get_all_addresses(db=db)

    if all_addresses is None:
        raise HTTPException(status_code=404, detail="Addresses list is empty")
    
    return all_addresses
