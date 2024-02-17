from typing import List, Type

import loguru
from sqlalchemy import not_
from sqlalchemy.orm import Session

from customer_support_api import models
from customer_support_api import schemas


def create_customer(
    session: Session, customer_in: schemas.CustomerCreate
) -> models.Customer:
    customer = models.Customer(**customer_in.model_dump())
    session.add(customer)
    session.commit()
    return customer


def get_customer(session: Session, customer_id: int) -> models.Customer | None:
    return session.get(models.Customer, customer_id)


def update_customer(
    session: Session,
    customer: models.Customer,
    customer_update: schemas.CustomerUpdate,
) -> models.Customer:
    for name, value in customer_update.model_dump(exclude_unset=True).items():
        setattr(customer, name, value)
    session.commit()
    return customer


def delete_customer(session: Session, customer: models.Customer) -> None:
    customer.is_deleted = True
    session.add(customer)
    session.commit()


def get_customers(
    session: Session, show_deleted=False, **kwargs
) -> List[Type[models.Customer]]:
    customers_query = session.query(models.Customer)
    for key, value in kwargs.items():
        try:
            customers_query = customers_query.filter(
                getattr(models.Customer, key) == value
            )
        except AttributeError:
            loguru.logger.warning(f"Unknown field '{key}'")
            return []
    if not show_deleted:
        customers_query = customers_query.filter(
            not_(models.Customer.is_deleted)
        )

    return customers_query.all()