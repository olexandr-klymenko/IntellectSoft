from sqlalchemy.orm import Session

from customer_support_api.models import Customer
from customer_support_api.v1.schemas import CustomerCreate, CustomerUpdate


def create_customer(session: Session, customer_in: CustomerCreate) -> Customer:
    customer = Customer(**customer_in.model_dump())
    session.add(customer)
    session.commit()
    return customer


def get_customer(session: Session, customer_id: int) -> Customer | None:
    return session.get(Customer, customer_id)


def update_customer(
    session: Session,
    customer: Customer,
    customer_update: CustomerUpdate,
) -> Customer:
    for name, value in customer_update.model_dump(exclude_unset=True).items():
        setattr(customer, name, value)
    session.commit()
    return customer


def delete_customer(session: Session, customer: Customer) -> None:
    session.delete(customer)
    session.commit()
