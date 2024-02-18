from typing import List, Type

import loguru
from sqlalchemy import not_
from sqlalchemy.orm import Session

import enums
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
    """
    As far as being a risky operation
    real customer deletion from the database is beyond of scope of API.
    Instead, we mark user as deleted.
    Also, we archive all corresponding requests.
    """
    customer.is_deleted = True
    session.add(customer)
    if customer.requests:
        for request in customer.requests:
            request.status = enums.RequestStatus.ARCHIVED
        session.add_all(customer.requests)
    session.commit()


def get_customers(
    session: Session, show_deleted=False, **kwargs
) -> List[Type[models.Customer]]:
    """
    By using kwargs we enable multiple filtering
    """
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
