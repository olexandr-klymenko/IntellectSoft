from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from customer_support_api.db_helper import db_helper
from customer_support_api.models import CustomerModel
from customer_support_api.v1 import crud, schemas

scoped_session_dependency = db_helper.scoped_session


def customer_by_id(
    customer_id: int,
    session: Session = Depends(scoped_session_dependency),
) -> CustomerModel:
    customer = crud.get_customer(session=session, customer_id=customer_id)
    if customer is not None:
        return customer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Customer {customer_id} not found!",
    )


def customer_query_params(
    first_name: str = Query(default=None),
    last_name: str = Query(default=None),
    phone: str = Query(default=None),
) -> schemas.CustomerUpdate:
    return schemas.CustomerUpdate(
        first_name=first_name, last_name=last_name, phone=phone
    )
