from typing import Optional

from sqlalchemy.orm import Session

from customer_support_api.models import Client
from customer_support_api.v1.schemas import ClientCreate, ClientUpdate


def create_client(session: Session, client_in: ClientCreate) -> Client:
    client = Client(**client_in.model_dump())
    session.add(client)
    session.commit()
    # session.refresh(client)
    return client


def get_client(session: Session, client_id: int) -> Optional[Client]:
    return session.get(Client, client_id)


def update_client(
    session: Session,
    client: Client,
    client_update: ClientUpdate,
) -> Client:
    for name, value in client_update.model_dump(exclude_unset=True).items():
        setattr(client, name, value)
    session.commit()
    return client


def delete_client(session: Session, client: Client) -> None:
    session.delete(client)
    session.commit()
