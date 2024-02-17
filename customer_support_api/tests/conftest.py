import pytest

from customer_support_api import enums, models
from customer_support_api.db_helper import DatabaseHelper

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

TEST_REQUESTS = [
    {"body": "Something wrong"},
    {"body": "Something wrong", "status": enums.RequestStatus.IN_PROGRESS},
    {"body": "Something wrong", "status": enums.RequestStatus.COMPLETED},
    {"body": "Something wrong", "status": enums.RequestStatus.REJECTED},
]

TEST_OPERATOR = {
    "first_name": "Peter",
    "last_name": "Falk",
}


@pytest.fixture
def session():
    models.BaseModel.metadata.create_all(db_helper.engine)
    session = db_helper.session_factory()
    yield session
    session.close()
    models.BaseModel.metadata.drop_all(db_helper.engine)


@pytest.fixture
def customer(session):
    customer = models.Customer(**TEST_CUSTOMER)
    session.add(customer)
    session.commit()
    yield customer


@pytest.fixture
def customers(session):
    customers = [models.Customer(**c) for c in TEST_CUSTOMERS]
    session.add_all(customers)
    session.commit()
    yield customers


@pytest.fixture
def customer_request(session, customer):
    request = models.Request(created_by=customer.id, **TEST_REQUEST)
    session.add(request)
    session.commit()
    yield request


@pytest.fixture
def customer_requests(session, customer):
    requests = [
        models.Request(created_by=customer.id, **r) for r in TEST_REQUESTS
    ]
    session.add_all(requests)
    session.commit()
    yield requests


@pytest.fixture
def operator(session):
    operator = models.Operator(**TEST_OPERATOR)
    session.add(operator)
    session.commit()
    yield operator
