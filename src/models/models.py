from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime as dt

from src.db.database import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    line_1 = Column(String, index=True)
    line_2 = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)

    resident = relationship("Customer", back_populates="address")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    address_id = Column(Integer, ForeignKey("addresses.id"))

    address = relationship("Address", back_populates="resident")
    order = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    payment_method = Column(String, index=True)
    start_date = Column(DateTime, default=dt.datetime.utcnow, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)
    brand = Column(String, index=True)
    state = Column(String, index=True)

    customer = relationship("Customer", back_populates="order")




