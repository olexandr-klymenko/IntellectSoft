from sqlalchemy.orm import Session

from customer_support_api import models
from customer_support_api import schemas


def create_operator(
    session: Session, operator_in: schemas.OperatorCreate
) -> models.Operator:
    operator = models.Operator(**operator_in.model_dump())
    session.add(operator)
    session.commit()
    return operator


def get_operator(session: Session, operator_id: int) -> models.Operator | None:
    return session.get(models.Operator, operator_id)
