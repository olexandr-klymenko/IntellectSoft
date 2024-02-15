from pydantic import BaseModel


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    phone: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientCreate):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
