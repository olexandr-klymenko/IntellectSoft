from typing import List, Type

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


def get_all_operators(session: Session) -> List[Type[models.Operator]]:
    requests_query = session.query(models.Operator)
    return requests_query.all()
