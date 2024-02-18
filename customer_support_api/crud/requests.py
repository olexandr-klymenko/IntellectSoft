from typing import List, Type

import loguru
from enums import RequestStatus
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from customer_support_api import models
from customer_support_api import schemas


def create_request(
    session: Session,
    customer: models.Customer,
    request_in: schemas.RequestCreate,
) -> models.Request:
    request = models.Request(created_by=customer.id, **request_in.model_dump())
    session.add(request)
    session.commit()
    return request


def get_request(session: Session, request_id: int) -> models.Request | None:
    return session.get(models.Request, request_id)


def update_request_body(
    session: Session, request: models.Request, body: str
) -> models.Request:
    request.body = body
    session.add(request)
    session.commit()
    return request


def assign_request(
    session: Session, request: models.Request, operator: models.Operator
) -> models.Request:
    """Assign request to an operator"""
    request.processed_by = operator.id
    request.status = RequestStatus.IN_PROGRESS
    session.add(request)
    session.commit()
    return request


def complete_reject_request(
    session: Session,
    request: models.Request,
    update_request_in: schemas.RequestCompleteReject,
):
    """
    Complete or reject request operation.
    These were unified due to similarity of condition and schema.
    Completing and rejecting request require that current state is IN_PROGRESS
    and mandatory comment field.
    """
    if request.status == RequestStatus.IN_PROGRESS:
        request.status = update_request_in.status
        request.resolution_comment = update_request_in.comment
        session.commit()
        return request

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Updating request from status '{request.status}'"
        f" to status '{update_request_in.status}' is not allowed!",
    )


def archive_request(session: Session, request: models.Request):
    """
    Archive request.
    Actual deletion from database is beyond the scope of the API.
    """
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
) -> List[Type[models.Request]]:
    requests_query = session.query(models.Request)
    for key, value in kwargs.items():
        try:
            requests_query = requests_query.filter(
                getattr(models.Request, key) == value
            )
        except AttributeError:
            loguru.logger.warning(f"Unknown field '{key}'")
            return []
    if not show_archived:
        requests_query = requests_query.filter(
            models.Request.status != RequestStatus.ARCHIVED
        )

    return requests_query.all()


def get_requests_by_customer(
    session: Session,
    customer: models.Customer,
    show_archived=False,
) -> List[Type[models.Request]]:
    return get_all_requests(
        session=session, show_archived=show_archived, created_by=customer.id
    )
