from sqlalchemy.orm import Session

from customer_support_api.models import Operator
from customer_support_api.v1.schemas import OperatorCreate


def create_operator(session: Session, operator_in: OperatorCreate) -> Operator:
    try:
        operator_in = Operator(**operator_in.model_dump())
        session.add(operator_in)
        session.commit()
        return operator_in
    except Exception as e:
        session.rollback()
        raise e


def get_operator(session: Session, operator_id: int) -> Operator | None:
    return session.get(Operator, operator_id)
