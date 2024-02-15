from pydantic import BaseModel


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerCreate):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
