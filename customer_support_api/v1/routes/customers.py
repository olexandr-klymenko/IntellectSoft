from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from customer_support_api.dependency import (
    customer_by_id,
    customer_query_params,
    scoped_session_dependency,
)
from customer_support_api.models import CustomerModel
from customer_support_api.v1 import crud, schemas

router = APIRouter(tags=["Customers"], prefix="/customers")


@router.post(
    "/",
    response_model=schemas.Customer,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer_in: schemas.CustomerCreate,
    session: Session = Depends(scoped_session_dependency),
):
    return crud.create_customer(session=session, customer_in=customer_in)


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(
    customer: CustomerModel = Depends(customer_by_id),
):
    return customer


@router.patch("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_update: schemas.CustomerUpdate,
    customer: CustomerModel = Depends(customer_by_id),
    session: Session = Depends(scoped_session_dependency),
):
    return crud.update_customer(
        session=session,
        customer=customer,
        customer_update=customer_update,
    )


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer: CustomerModel = Depends(customer_by_id),
    session: Session = Depends(scoped_session_dependency),
) -> None:
    crud.delete_customer(session=session, customer=customer)


@router.get("/", response_model=List[schemas.Customer])
def get_customers(
    customer_args: schemas.CustomerUpdate = Depends(customer_query_params),
    show_deleted: bool = Query(default=False),
    session: Session = Depends(scoped_session_dependency),
):
    return crud.get_customers(
        session=session,
        show_deleted=show_deleted,
        **customer_args.model_dump(exclude_none=True)
    )
