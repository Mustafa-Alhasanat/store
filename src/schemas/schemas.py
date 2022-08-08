from enum import Enum
from pydantic import BaseModel
import datetime as dt


# ------ Address schemas ------

class AddressBase(BaseModel):
    country: str
    city: str
    line_1: str 
    line_2: str 

class AddressCreate(AddressBase):
    pass

class AddressSchema(AddressBase):
    id: int
    
    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "country": "Jordan",
                "city": "Balqa",
                "line_1": "st. 20",
                "line_2": "apt. 20"
            }
        }


# ------ Customer schemas ------

class CustomerBase(BaseModel):
    first_name: str
    last_name: str 
    email: str 

class CustomerCreate(CustomerBase):
    address: AddressBase

class CustomerSchema(CustomerBase):
    id: int
    created_at: dt.datetime
    address_id: int
    
    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "first_name": "Mustafa",
                "last_name": "Hasanat",
                "email": "m@m.com",
                "country": "Jordan",
                "city": "Balqa",
                "line_1": "st. 20",
                "line_2": "apt. 20"
            }
        }


# ------ Order schemas ------

class PaymentMethod(str, Enum):
    visa = "visa"
    paypal = "paypal"
    amazonPay = "amazonPay"

class State(str, Enum):
    active = "active"
    canceled = "canceled"
    suspended = "suspended"

class OrderBase(BaseModel):
    payment_method: PaymentMethod 
    brand: str
    state: State

class OrderCreate(OrderBase):
    pass

class OrderSchema(OrderBase):
    id: int
    start_date: dt.datetime
    customer_id: int
    
    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "payment_method": "visa", 
                "brand": "mac",
                "state": "active"
            }
        }

