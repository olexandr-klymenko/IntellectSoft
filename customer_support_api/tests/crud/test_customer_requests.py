from customer_support_api.models import RequestModel, RequestStateEnum
from customer_support_api.tests.conftest import TEST_REQUEST
from customer_support_api.v1.crud import (
    assign_request,
    complete_request,
    create_request,
    get_request,
    reject_request,
)
from customer_support_api.v1.schemas import RequestCreate


def test_create_request(session, customer):
    res_request = create_request(
        session=session,
        customer=customer,
        request_in=RequestCreate(**TEST_REQUEST),
    )
    db_request = session.get(RequestModel, res_request.id)
    assert db_request.status == RequestStateEnum.PENDING
    assert db_request.body == TEST_REQUEST["body"]


def test_get_request(session, customer, customer_request):
    res_request = get_request(session=session, request_id=customer_request.id)
    assert res_request.created_by == customer_request.created_by


def test_assign_request(session, customer, customer_request, operator):
    assign_request(
        session=session, request=customer_request, operator=operator
    )
    db_request = session.get(RequestModel, customer_request.id)
    assert db_request.processed_by == operator.id
    assert db_request.status == RequestStateEnum.IN_PROGRESS


def test_complete_request(session, customer, customer_request, operator):
    customer_request.status = RequestStateEnum.IN_PROGRESS
    session.add(customer_request)
    session.commit()
    complete_request(
        session=session,
        request=customer_request,
        comment="The issue has been resolved",
    )
    db_request = session.get(RequestModel, customer_request.id)
    assert db_request.status == RequestStateEnum.COMPLETED


def test_reject_request(session, customer, customer_request, operator):
    customer_request.status = RequestStateEnum.IN_PROGRESS
    session.add(customer_request)
    session.commit()
    reject_request(
        session=session,
        request=customer_request,
        comment="The issue won't be resolved",
    )
    db_request = session.get(RequestModel, customer_request.id)
    assert db_request.status == RequestStateEnum.REJECTED
