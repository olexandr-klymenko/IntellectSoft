from customer_support_api.models import Client
from customer_support_api.v1.crud import (
    create_client,
    delete_client,
    get_client,
    update_client,
)
from customer_support_api.v1.schemas import ClientCreate, ClientUpdate


def test_create_client(session):
    client = create_client(
        session=session,
        client_in=ClientCreate(first_name="John", last_name="Smith", phone="1231231"),
    )

    db_client = session.get(Client, client.id)
    assert db_client.id == client.id


def test_get_client(session, client):
    res_client = get_client(session=session, client_id=client.id)
    assert res_client.phone == client.phone


def test_update_client(session, client):
    new_phone = "55555"
    update_client(
        session=session,
        client=client,
        client_update=ClientUpdate(phone=new_phone),
    )
    db_client = session.get(Client, client.id)
    assert db_client.phone == new_phone
    assert db_client.first_name == client.first_name


def test_delete_client(session, client):
    delete_client(session=session, client=client)
    db_client = session.get(Client, client.id)
    assert db_client is None
