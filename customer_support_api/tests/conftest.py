import pytest

from customer_support_api.db_helper import DatabaseHelper
from customer_support_api.models import BaseModel, CustomerModel, RequestModel

db_helper = DatabaseHelper(url="sqlite:///:memory:")

TEST_CUSTOMER = {
    "first_name": "John",
    "last_name": "Smith",
    "phone": "+442083661177",
}

TEST_CUSTOMERS = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "phone": "+442083661171",
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "phone": "+442083661172",
    },
    {
        "first_name": "Charlie",
        "last_name": "Williams",
        "phone": "+442083661173",
    },
    {
        "first_name": "Diana",
        "last_name": "Brown",
        "phone": "+442083661174",
    },
    {
        "first_name": "Evan",
        "last_name": "Jones",
        "phone": "+442083661175",
    },
]

TEST_REQUEST = {"body": "Something wrong"}


INVALID_PHONE_NUMBER = "555444111"


@pytest.fixture
def session():
    BaseModel.metadata.create_all(db_helper.engine)
    session = db_helper.session_factory()
    yield session
    session.close()
    BaseModel.metadata.drop_all(db_helper.engine)


@pytest.fixture
def customer(session):
    customer = CustomerModel(**TEST_CUSTOMER)
    session.add(customer)
    session.commit()
    yield customer


@pytest.fixture
def customers(session):
    customers = [CustomerModel(**c) for c in TEST_CUSTOMERS]
    session.add_all(customers)
    session.commit()
    yield customers


@pytest.fixture
def customer_request(session, customer):
    request = RequestModel(created_by=customer.id, **TEST_REQUEST)
    session.add(request)
    session.commit()
    yield request
