from typing import List, Type

from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from customer_support_api.models import Customer
from customer_support_api.v1.schemas import CustomerCreate, CustomerUpdate


def create_customer(session: Session, customer_in: CustomerCreate) -> Customer:
    try:
        customer = Customer(**customer_in.model_dump())
        session.add(customer)
        session.commit()
        return customer
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid customer: {str(e)}!",
        )


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


def get_customers(session: Session, **kwargs) -> List[Type[Customer]]:
    customers_query = session.query(Customer)
    for key, value in kwargs.items():
        try:
            customers_query = customers_query.filter(
                getattr(Customer, key) == value
            )
        except AttributeError:
            print(f"Unknown field '{key}'")
            return []

    return customers_query.all()
