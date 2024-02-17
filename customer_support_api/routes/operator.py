from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from customer_support_api import crud
from customer_support_api import dependency
from customer_support_api import models
from customer_support_api import schemas

router = APIRouter(tags=["Operators"], prefix="/operators")


@router.post(
    "/",
    response_model=schemas.Operator,
    status_code=status.HTTP_201_CREATED,
)
def create_operator(
    operator_in: schemas.OperatorCreate,
    session: Session = Depends(dependency.scoped_session),
):
    return crud.create_operator(session=session, operator_in=operator_in)


@router.patch(
    "/{operator_id}/requests/{request_id}", response_model=schemas.Request
)
def assign_request(
    request: models.Request = Depends(dependency.request_by_id),
    operator: models.Operator = Depends(dependency.operator_by_id),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.assign_request(
        session=session,
        request=request,
        operator=operator,
    )
