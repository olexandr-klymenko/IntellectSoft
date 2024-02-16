from typing import List, Type

import loguru
from sqlalchemy import not_
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
    update_customer(
        session=session,
        customer=customer,
        customer_update=CustomerUpdate(is_deleted=True),
    )


def get_customers(
    session: Session, show_deleted=False, **kwargs
) -> List[Type[CustomerModel]]:
    customers_query = session.query(CustomerModel)
    for key, value in kwargs.items():
        try:
            customers_query = customers_query.filter(
                getattr(CustomerModel, key) == value
            )
        except AttributeError:
            loguru.logger.warning(f"Unknown field '{key}'")
            return []
    if not show_deleted:
        customers_query = customers_query.filter(
            not_(CustomerModel.is_deleted)
        )

    return customers_query.all()
