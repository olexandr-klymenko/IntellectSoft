import pytest

from customer_support_api.db_helper import DatabaseHelper
from customer_support_api.models import Base, Customer

db_helper = DatabaseHelper(url="sqlite:///:memory:")

TEST_CUSTOMER = {
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
def customer(session):
    """Fixture for test customer"""
    customer = Customer(**TEST_CUSTOMER)
    session.add(customer)
    session.commit()
    yield customer
