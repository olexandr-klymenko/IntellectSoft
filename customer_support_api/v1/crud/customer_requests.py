from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from customer_support_api.models import (
    CustomerModel,
    OperatorModel,
    RequestModel,
    RequestStateEnum,
)
from customer_support_api.v1.schemas import RequestCreate


def create_request(
    session: Session, customer: CustomerModel, request_in: RequestCreate
) -> RequestModel:
    try:
        request = RequestModel(
            created_by=customer.id, **request_in.model_dump()
        )
        session.add(request)
        session.commit()
        return request
    except Exception as e:
        session.rollback()
        raise e


def get_request(session: Session, request_id: int) -> RequestModel | None:
    return session.get(RequestModel, request_id)


def update_request_body(session: Session, request: RequestModel, body: str):
    request.body = body
    session.add(request)
    session.commit()


def assign_request(
    session: Session, request: RequestModel, operator: OperatorModel
) -> None:
    request.processed_by = operator.id
    request.status = RequestStateEnum.IN_PROGRESS
    session.add(request)
    session.commit()


def complete_request(session: Session, request: RequestModel, comment: str):
    if request.status == RequestStateEnum.IN_PROGRESS:
        request.status = RequestStateEnum.COMPLETED
        request.resolution_comment = comment
        session.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Completing request "
        f"with status '{request.status}' is not allowed!",
    )


def reject_request(session: Session, request: RequestModel, comment: str):
    if request.status == RequestStateEnum.IN_PROGRESS:
        request.status = RequestStateEnum.REJECTED
        request.resolution_comment = comment
        session.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Rejecting request"
        f" with status '{request.status}' is not allowed!",
    )


def archive_request(session: Session, request: RequestModel):
    if request.status in (
        RequestStateEnum.COMPLETED,
        RequestStateEnum.REJECTED,
    ):
        request.status = RequestStateEnum.ARCHIVED
        session.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Archiving request"
        f" with status '{request.status}' is not allowed!",
    )
