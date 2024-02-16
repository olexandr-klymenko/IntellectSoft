from typing import List, Type

import loguru
from sqlalchemy.orm import Session

from customer_support_api.models import CustomerModel
from customer_support_api.v1.schemas import CustomerCreate, CustomerUpdate


def create_customer(
    session: Session, customer_in: CustomerCreate
) -> CustomerModel:
    try:
        customer = CustomerModel(**customer_in.model_dump())
        session.add(customer)
        session.commit()
        return customer
    except Exception as e:
        session.rollback()
        raise e


def get_customer(session: Session, customer_id: int) -> CustomerModel | None:
    return session.get(CustomerModel, customer_id)


def update_customer(
    session: Session,
    customer: CustomerModel,
    customer_update: CustomerUpdate,
) -> CustomerModel:
    try:
        for name, value in customer_update.model_dump(
            exclude_unset=True
        ).items():
            setattr(customer, name, value)
        session.commit()
        return customer
    except Exception as e:
        session.rollback()
        raise e


def delete_customer(session: Session, customer: CustomerModel) -> None:
    session.delete(customer)
    session.commit()


def get_customers(session: Session, **kwargs) -> List[Type[CustomerModel]]:
    customers_query = session.query(CustomerModel)
    for key, value in kwargs.items():
        try:
            customers_query = customers_query.filter(
                getattr(CustomerModel, key) == value
            )
        except AttributeError:
            loguru.logger.warning(f"Unknown field '{key}'")
            return []

    return customers_query.all()
