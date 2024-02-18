import pytest
from fastapi import HTTPException

from customer_support_api import crud
from customer_support_api import enums
from customer_support_api import models
from customer_support_api import schemas


def test_create_request(session, customer):
    res_request = crud.create_request(
        session=session,
        customer=customer,
        request_in=schemas.RequestCreate(**{"body": "Something wrong"}),
    )
    db_request = session.get(models.Request, res_request.id)
    assert db_request.status == enums.RequestStatus.PENDING
    assert db_request.body == "Something wrong"


def test_get_request(session, customer, customer_request):
    res_request = crud.get_request(
        session=session, request_id=customer_request.id
    )
    assert res_request.created_by == customer_request.created_by


def test_assign_request(session, customer, customer_request, operator):
    crud.assign_request(
        session=session, request=customer_request, operator=operator
    )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.processed_by == operator.id
    assert db_request.status == enums.RequestStatus.IN_PROGRESS


def test_complete_request(session, customer, customer_request, operator):
    customer_request.status = enums.RequestStatus.IN_PROGRESS
    session.add(customer_request)
    session.commit()
    crud.complete_reject_request(
        session=session,
        request=customer_request,
        update_request_in=schemas.RequestCompleteReject(
            status="COMPLETED",
            resolution_comment="The issue has been resolved",
        ),
    )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.status == enums.RequestStatus.COMPLETED


def test_complete_request_fail(session, customer, customer_request, operator):
    with pytest.raises(HTTPException):
        crud.complete_reject_request(
            session=session,
            request=customer_request,
            update_request_in=schemas.RequestCompleteReject(
                status="COMPLETED",
                resolution_comment="The issue has been resolved",
            ),
        )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.status == enums.RequestStatus.PENDING


def test_reject_request(session, customer, customer_request, operator):
    customer_request.status = enums.RequestStatus.IN_PROGRESS
    session.add(customer_request)
    session.commit()
    crud.complete_reject_request(
        session=session,
        request=customer_request,
        update_request_in=schemas.RequestCompleteReject(
            status="REJECTED",
            resolution_comment="The issue won't be resolved",
        ),
    )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.status == enums.RequestStatus.REJECTED


def test_reject_request_fail(session, customer, customer_request, operator):
    with pytest.raises(HTTPException):
        crud.complete_reject_request(
            session=session,
            request=customer_request,
            update_request_in=schemas.RequestCompleteReject(
                status="REJECTED",
                resolution_comment="The issue won't be resolved",
            ),
        )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.status == enums.RequestStatus.PENDING


def test_archive_request(session, customer_request):
    customer_request.status = enums.RequestStatus.COMPLETED
    session.add(customer_request)
    session.commit()
    crud.archive_request(
        session=session,
        request=customer_request,
    )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.status == enums.RequestStatus.ARCHIVED


def test_archive_request_fail(session, customer_request):
    with pytest.raises(HTTPException):
        crud.archive_request(
            session=session,
            request=customer_request,
        )
    db_request = session.get(models.Request, customer_request.id)
    assert db_request.status == enums.RequestStatus.PENDING


def test_requests_by_customer(session, customer, customer_requests):
    new_request = models.Request(
        created_by=customer.id,
        body="Test description",
        status=enums.RequestStatus.ARCHIVED,
    )
    session.add(new_request)
    session.commit()
    requests = crud.get_requests_by_customer(
        session=session, customer=customer
    )
    assert len(requests) == len(customer_requests)


def test_requests_by_customer_show_archived(
    session, customer, customer_requests
):
    new_request = models.Request(
        created_by=customer.id,
        body="Test description",
        status=enums.RequestStatus.ARCHIVED,
    )
    session.add(new_request)
    session.commit()
    requests = crud.get_requests_by_customer(
        session=session, customer=customer, show_archived=True
    )
    assert len(requests) == len(session.query(models.Request).all())
