import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr


class StateEnum(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id = Column(Integer, primary_key=True)


class Customer(Base):
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    phone = Column(String(length=50))


class Request(Base):
    created_by = Column(Integer, ForeignKey("customer.id"))
    body = Column(String(length=256), nullable=False)
    status = Column(Enum(StateEnum))
    processed_by = Column(Integer, ForeignKey("operator.id"))


class Operator(Base):
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
