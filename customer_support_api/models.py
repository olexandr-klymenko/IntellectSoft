import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship


class StateEnum(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"

    id = Column(Integer, primary_key=True)


class CustomerModel(BaseModel):
    __tablename__ = "customer"

    first_name = Column(String(length=50), index=True)
    last_name = Column(String(length=50), index=True)
    phone = Column(String(length=13), unique=True)

    requests = relationship("RequestModel", backref="customer", lazy=True)


class RequestModel(BaseModel):
    __tablename__ = "request"

    created_by = Column(
        Integer,
        ForeignKey("customer.id", ondelete="SET NULL"),
    )
    body = Column(String(length=256), nullable=False)
    status = Column(Enum(StateEnum), default=StateEnum.PENDING)
    processed_by = Column(Integer, ForeignKey("operator.id"))
    resolution_comment = Column(String(length=256))


class OperatorModel(BaseModel):
    __tablename__ = "operator"

    first_name = Column(String(length=50))
    last_name = Column(String(length=50))

    requests = relationship("RequestModel", backref="operator", lazy=True)
