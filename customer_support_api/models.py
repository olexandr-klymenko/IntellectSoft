from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

from customer_support_api import enums


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class Customer(BaseModel):
    __tablename__ = "customer"

    first_name = Column(String(length=50), index=True)
    last_name = Column(String(length=50), index=True)
    phone = Column(String(length=13), unique=True)
    is_deleted = Column(Boolean, default=False)

    requests = relationship("Request", backref="customer", lazy=True)


class Request(BaseModel):
    __tablename__ = "request"

    created_by = Column(
        Integer,
        ForeignKey("customer.id", ondelete="SET NULL"),
    )
    body = Column(String(length=256), nullable=False)
    status = Column(
        Enum(enums.RequestStatus), default=enums.RequestStatus.PENDING
    )
    processed_by = Column(Integer, ForeignKey("operator.id"))
    resolution_comment = Column(String(length=256))


class Operator(BaseModel):
    __tablename__ = "operator"

    first_name = Column(String(length=50))
    last_name = Column(String(length=50))

    requests = relationship("Request", backref="operator", lazy=True)
