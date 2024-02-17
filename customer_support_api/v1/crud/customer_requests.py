from typing import List, Type

import loguru
import models
from enums import RequestStatus
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from customer_support_api.models import Customer, Operator, Request
from customer_support_api.v1 import schemas


def create_request(
    session: Session, customer: Customer, request_in: schemas.RequestCreate
) -> Request:
    request = Request(created_by=customer.id, **request_in.model_dump())
    session.add(request)
    session.commit()
    return request


def get_request(session: Session, request_id: int) -> Request | None:
    return session.get(Request, request_id)


def update_request_body(
    session: Session, request: Request, body: str
) -> models.Request:
    request.body = body
    session.add(request)
    session.commit()
    return request


def assign_request(
    session: Session, request: Request, operator: Operator
) -> models.Request:
    request.processed_by = operator.id
    request.status = RequestStatus.IN_PROGRESS
    session.add(request)
    session.commit()
    return request


def complete_reject_request(
    session: Session,
    request: Request,
    update_request_in: schemas.RequestCompleteReject,
    comment: str,
):
    if request.status == RequestStatus.IN_PROGRESS:
        request.status = update_request_in.status
        request.resolution_comment = comment
        session.commit()
        return request

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Updating request from status '{request.status}'"
        f" to status '{update_request_in.status}' is not allowed!",
    )


def archive_request(session: Session, request: Request):
    if request.status in (
        RequestStatus.COMPLETED,
        RequestStatus.REJECTED,
    ):
        request.status = RequestStatus.ARCHIVED
        session.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Archiving request"
        f" with status '{request.status}' is not allowed!",
    )


def get_all_requests(
    session: Session, show_archived=False, **kwargs
) -> List[Type[Request]]:
    requests_query = session.query(Request)
    for key, value in kwargs.items():
        try:
            requests_query = requests_query.filter(
                getattr(Request, key) == value
            )
        except AttributeError:
            loguru.logger.warning(f"Unknown field '{key}'")
            return []
    if not show_archived:
        requests_query = requests_query.filter(
            Request.status != RequestStatus.ARCHIVED
        )

    return requests_query.all()


def get_requests_by_customer(
    session: Session,
    customer: Customer,
    show_archived=False,
) -> List[Type[Request]]:
    return get_all_requests(
        session=session, show_archived=show_archived, created_by=customer.id
    )
