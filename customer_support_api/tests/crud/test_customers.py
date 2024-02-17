from customer_support_api import crud
from customer_support_api import models
from customer_support_api import schemas


def test_create_customer(session):
    customer = crud.create_customer(
        session=session,
        customer_in=schemas.CustomerCreate(
            **{
                "first_name": "John",
                "last_name": "Smith",
                "phone": "+442083661177",
            }
        ),
    )

    db_customer = session.get(models.Customer, customer.id)
    assert db_customer.phone == customer.phone


def test_get_customer(session, customer):
    res_customer = crud.get_customer(session=session, customer_id=customer.id)
    assert res_customer.phone == customer.phone


def test_update_customer(session, customer):
    new_phone = "+442083661175"
    crud.update_customer(
        session=session,
        customer=customer,
        customer_update=schemas.CustomerUpdate(phone=new_phone),
    )
    db_customer = session.get(models.Customer, customer.id)
    assert db_customer.phone == new_phone
    assert db_customer.first_name == customer.first_name


def test_delete_customer(session, customer):
    crud.delete_customer(session=session, customer=customer)
    db_customer = session.get(models.Customer, customer.id)
    assert db_customer.is_deleted


def test_get_all_customers(session, customers):
    customer = models.Customer(
        **{
            "first_name": "John",
            "last_name": "Smith",
            "phone": "+442083661177",
        }
    )
    customer.is_deleted = True
    session.add(customer)
    session.commit()
    res_customers = crud.get_customers(session)
    assert len(res_customers) == len(customers)


def test_get_all_customers_show_deleted(session, customers):
    customer = models.Customer(
        **{
            "first_name": "John",
            "last_name": "Smith",
            "phone": "+442083661177",
        }
    )
    customer.is_deleted = True
    session.add(customer)
    session.commit()
    res_customers = crud.get_customers(session, show_deleted=True)
    assert len(res_customers) == len(session.query(models.Customer).all())


def test_get_customers_by_first_name(session, customers):
    res_customers = crud.get_customers(session, first_name="Alice")
    assert (
        res_customers[0]
        == session.query(models.Customer)
        .filter(models.Customer.first_name == "Alice")
        .first()
    )


def test_get_customers_by_last_name(session, customers):
    res_customers = crud.get_customers(session, last_name="Jones")
    assert (
        res_customers[0]
        == session.query(models.Customer)
        .filter(models.Customer.phone == "+442083661175")
        .first()
    )


def test_get_customers_by_phone(session, customers):
    res_customers = crud.get_customers(session, phone="+442083661173")
    assert (
        res_customers[0]
        == session.query(models.Customer)
        .filter(models.Customer.first_name == "Charlie")
        .first()
    )


def test_get_customers_invalid_field(session, customers):
    res_customers = crud.get_customers(session, email="test@example.com")
    assert res_customers == []
