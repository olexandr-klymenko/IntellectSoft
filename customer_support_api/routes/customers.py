from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from customer_support_api import crud
from customer_support_api import dependency
from customer_support_api import models
from customer_support_api import schemas

router = APIRouter(tags=["Customers"], prefix="/customers")


@router.post(
    "/",
    response_model=schemas.Customer,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer_in: schemas.CustomerCreate,
    session: Session = Depends(dependency.scoped_session),
):
    return crud.create_customer(session=session, customer_in=customer_in)


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(
    customer: models.Customer = Depends(dependency.customer_by_id),
):
    return customer


@router.patch("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_update: schemas.CustomerUpdate,
    customer: models.Customer = Depends(dependency.customer_by_id),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.update_customer(
        session=session,
        customer=customer,
        customer_update=customer_update,
    )


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer: models.Customer = Depends(dependency.customer_by_id),
    session: Session = Depends(dependency.scoped_session),
) -> None:
    crud.delete_customer(session=session, customer=customer)


@router.get("/", response_model=List[schemas.Customer])
def get_customers(
    customer_args: schemas.CustomerUpdate = Depends(
        dependency.customers_query_params
    ),
    show_deleted: bool = Query(default=False),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.get_customers(
        session=session,
        show_deleted=show_deleted,
        **customer_args.model_dump(exclude_none=True)
    )


@router.post(
    "/{customer_id}/requests",
    response_model=schemas.Request,
    status_code=status.HTTP_201_CREATED,
)
def create_request_for_customer(
    request_in: schemas.RequestCreate,
    customer: models.Customer = Depends(dependency.customer_by_id),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.create_request(
        session=session, customer=customer, request_in=request_in
    )


@router.get(
    "/{customer_id}/requests",
    response_model=List[schemas.Request],
)
def get_requests_by_customer(
    customer: models.Customer = Depends(dependency.customer_by_id),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.get_requests_by_customer(session=session, customer=customer)
