from tests.conftest import TEST_CUSTOMER, TEST_REQUEST

from customer_support_api.models import CustomerModel, RequestModel, StateEnum
from customer_support_api.v1.crud import (
    create_customer,
    create_request,
    delete_customer,
    get_customer,
    get_customers,
    get_request,
    update_customer,
)
from customer_support_api.v1.schemas import (
    CustomerCreate,
    CustomerUpdate,
    RequestCreate,
)


def test_create_customer(session):
    customer = create_customer(
        session=session,
        customer_in=CustomerCreate(**TEST_CUSTOMER),
    )

    db_customer = session.get(CustomerModel, customer.id)
    assert db_customer.phone == customer.phone


def test_get_customer(session, customer):
    res_customer = get_customer(session=session, customer_id=customer.id)
    assert res_customer.phone == customer.phone


def test_update_customer(session, customer):
    new_phone = "+442083661175"
    update_customer(
        session=session,
        customer=customer,
        customer_update=CustomerUpdate(phone=new_phone),
    )
    db_customer = session.get(CustomerModel, customer.id)
    assert db_customer.phone == new_phone
    assert db_customer.first_name == customer.first_name


def test_delete_customer(session, customer):
    delete_customer(session=session, customer=customer)
    db_customer = session.get(CustomerModel, customer.id)
    assert db_customer is None


def test_delete_customer_with_requests(session, customer, customer_request):
    delete_customer(session=session, customer=customer)
    db_customer = session.get(CustomerModel, customer.id)
    db_request = session.get(RequestModel, customer_request.id)
    assert db_customer is None
    assert db_request.body == customer_request.body
    assert db_request.created_by is None


def test_get_all_customers(session, customers):
    res_customers = get_customers(session)
    assert len(res_customers) == len(session.query(CustomerModel).all())


def test_get_customers_by_first_name(session, customers):
    res_customers = get_customers(session, first_name="Alice")
    assert (
        res_customers[0]
        == session.query(CustomerModel)
        .filter(CustomerModel.first_name == "Alice")
        .first()
    )


def test_get_customers_by_last_name(session, customers):
    res_customers = get_customers(session, last_name="Jones")
    assert (
        res_customers[0]
        == session.query(CustomerModel)
        .filter(CustomerModel.phone == "+442083661175")
        .first()
    )


def test_get_customers_by_phone(session, customers):
    res_customers = get_customers(session, phone="+442083661173")
    assert (
        res_customers[0]
        == session.query(CustomerModel)
        .filter(CustomerModel.first_name == "Charlie")
        .first()
    )


def test_get_customers_invalid_field(session, customers):
    res_customers = get_customers(session, email="test@example.com")
    assert res_customers == []


def test_create_request(session, customer):
    res_request = create_request(
        session=session,
        customer_id=customer.id,
        request_in=RequestCreate(**TEST_REQUEST),
    )
    db_request = session.get(RequestModel, res_request.id)
    assert db_request.status == StateEnum.PENDING
    assert db_request.body == TEST_REQUEST["body"]


def test_get_request(session, customer, customer_request):
    res_request = get_request(session=session, request_id=customer_request.id)
    assert res_request.created_by == customer_request.created_by
