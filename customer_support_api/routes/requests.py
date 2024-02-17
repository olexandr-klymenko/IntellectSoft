from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from customer_support_api import crud
from customer_support_api import dependency
from customer_support_api import models
from customer_support_api import schemas

router = APIRouter(tags=["Requests"], prefix="/requests")


@router.get("/{request_id}", response_model=schemas.Request)
def get_request(
    request: models.Request = Depends(dependency.request_by_id),
):
    return request


@router.patch("/{request_id}", response_model=schemas.Request)
def update_request_body(
    body: str,
    request: models.Request = Depends(dependency.request_by_id),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.update_request_body(
        session=session,
        request=request,
        body=body,
    )


@router.get("/", response_model=List[schemas.Request])
def get_requests(
    requests_args: schemas.RequestUpdate = Depends(
        dependency.requests_query_params
    ),
    show_archived: bool = Query(default=False),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.get_all_requests(
        session=session,
        show_archived=show_archived,
        **requests_args.model_dump(exclude_none=True)
    )


@router.patch("/{request_id}", response_model=schemas.Request)
def complete_reject_request(
    update_request_in: schemas.RequestCompleteReject,
    comment: str,
    request: models.Request = Depends(dependency.request_by_id),
    session: Session = Depends(dependency.scoped_session),
):
    return crud.complete_reject_request(
        session=session,
        request=request,
        update_request_in=update_request_in,
        comment=comment,
    )


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_request(
    request: models.Request = Depends(dependency.request_by_id),
    session: Session = Depends(dependency.scoped_session),
) -> None:
    crud.archive_request(session=session, request=request)
