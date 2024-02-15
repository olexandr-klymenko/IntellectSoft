from customer_support_api.models import Customer
from customer_support_api.v1.crud import (
    create_customer,
    delete_customer,
    get_customer,
    update_customer,
)
from customer_support_api.v1.schemas import CustomerCreate, CustomerUpdate


def test_create_customer(session):
    customer = create_customer(
        session=session,
        customer_in=CustomerCreate(
            first_name="John", last_name="Smith", phone="1231231"
        ),
    )

    db_customer = session.get(Customer, customer.id)
    assert db_customer.id == customer.id


def test_get_customer(session, customer):
    res_customer = get_customer(session=session, customer_id=customer.id)
    assert res_customer.phone == customer.phone


def test_update_customer(session, customer):
    new_phone = "55555"
    update_customer(
        session=session,
        customer=customer,
        customer_update=CustomerUpdate(phone=new_phone),
    )
    db_customer = session.get(Customer, customer.id)
    assert db_customer.phone == new_phone
    assert db_customer.first_name == customer.first_name


def test_delete_customer(session, customer):
    delete_customer(session=session, customer=customer)
    db_customer = session.get(Customer, customer.id)
    assert db_customer is None
