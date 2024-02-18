from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from customer_support_api.db_helper import db_helper
from customer_support_api import enums
from customer_support_api import crud
from customer_support_api import models
from customer_support_api import schemas

scoped_session = db_helper.scoped_session


def customer_by_id(
    customer_id: int,
    session: Session = Depends(scoped_session),
) -> models.Customer:
    customer = crud.get_customer(session=session, customer_id=customer_id)
    if customer is not None:
        return customer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Customer {customer_id} not found!",
    )


def request_by_id(
    request_id: int,
    session: Session = Depends(scoped_session),
) -> models.Request:
    request = crud.get_request(session=session, request_id=request_id)
    if request is not None:
        return request

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Request {request_id} not found!",
    )


def operator_by_id(
    operator_id: int,
    session: Session = Depends(scoped_session),
) -> models.Operator:
    operator = crud.get_operator(session=session, operator_id=operator_id)
    if operator is not None:
        return operator

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Operator {operator_id} not found!",
    )


def customers_query_params(
    first_name: str = Query(default=None),
    last_name: str = Query(default=None),
    phone: str = Query(default=None),
) -> schemas.CustomerUpdate:
    return schemas.CustomerUpdate(
        first_name=first_name, last_name=last_name, phone=phone
    )


def requests_query_params(
    request_status: enums.RequestStatus = Query(default=None),
    processed_by: int = Query(default=None),
) -> schemas.RequestQueryArgs:
    return schemas.RequestQueryArgs(
        status=request_status, processed_by=processed_by
    )
