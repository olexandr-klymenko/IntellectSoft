from sqlalchemy.orm import Session

from customer_support_api.models import OperatorModel
from customer_support_api.v1.schemas import OperatorCreate


def create_operator(
    session: Session, operator: OperatorCreate
) -> OperatorModel:
    try:
        operator = OperatorModel(**operator.model_dump())
        session.add(operator)
        session.commit()
        return operator
    except Exception as e:
        session.rollback()
        raise e
