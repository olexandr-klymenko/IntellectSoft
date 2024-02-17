from typing import List, Type

import loguru
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
    request = RequestModel(created_by=customer.id, **request_in.model_dump())
    session.add(request)
    session.commit()
    return request


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


def get_all_requests(
    session: Session, show_archived=False, **kwargs
) -> List[Type[RequestModel]]:
    requests_query = session.query(RequestModel)
    for key, value in kwargs.items():
        try:
            requests_query = requests_query.filter(
                getattr(RequestModel, key) == value
            )
        except AttributeError:
            loguru.logger.warning(f"Unknown field '{key}'")
            return []
    if not show_archived:
        requests_query = requests_query.filter(
            RequestModel.status != RequestStateEnum.ARCHIVED
        )

    return requests_query.all()


def get_requests_by_customer(
    session: Session,
    customer: CustomerModel,
    show_archived=False,
) -> List[Type[RequestModel]]:
    return get_all_requests(
        session=session, show_archived=show_archived, created_by=customer.id
    )
