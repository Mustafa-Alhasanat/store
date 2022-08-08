from fastapi import Depends
from sqlalchemy.orm import Session

from src.models.models import Address
from src.schemas.schemas import AddressCreate


def get_address_by_id(address_id: int, db: Session):
    return db.query(Address).filter(Address.id == address_id).first()

def get_all_addresses(db: Session):
    return db.query(Address).all()

def create_address(address: AddressCreate, db: Session):
    address_object = Address(
        line_1=address.line_1,
        line_2=address.line_2,
        city=address.city,
        country=address.country
    )

    db.add(address_object)
    db.commit()
    db.refresh(address_object)

    return address_object

def delete_address(address_id: int, db:Session):
    address_object = get_address_by_id(address_id=address_id, db=db)
    db.delete(address_object)
    db.commit()

    