import pytest

from customer_support_api.db_helper import DatabaseHelper
from customer_support_api.models import Base, Client

db_helper = DatabaseHelper(url="sqlite:///:memory:")

TEST_CLIENT = {
    "first_name": "John",
    "last_name": "Smith",
    "phone": "1231231",
}


@pytest.fixture
def session():
    Base.metadata.create_all(db_helper.engine)
    session = db_helper.session_factory()
    yield session
    session.close()
    Base.metadata.drop_all(db_helper.engine)


@pytest.fixture
def client(session):
    client = Client(**TEST_CLIENT)
    session.add(client)
    session.commit()
    yield client
