import phonenumbers
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from customer_support_api.enums import CompletedRejected, RequestStatus


def phone_number_validator(v: str):
    try:
        phone_number_obj = phonenumbers.parse(v, None)
        if not phonenumbers.is_valid_number(phone_number_obj):
            raise ValueError("Invalid phone number")
    except phonenumbers.NumberParseException as e:
        raise ValueError("Invalid phone number format") from e

    return phonenumbers.format_number(
        phone_number_obj, phonenumbers.PhoneNumberFormat.E164
    )


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str = Field(..., example="+442083661177")


class CustomerCreate(CustomerBase):
    phone: Annotated[str, BeforeValidator(phone_number_validator)]


class Customer(CustomerBase):
    id: int


class CustomerUpdate(CustomerCreate):
    first_name: str | None = None
    last_name: str | None = None
    phone: Annotated[
        str, BeforeValidator(phone_number_validator)
    ] | None = None


class RequestBase(BaseModel):
    body: str


class RequestCreate(RequestBase):
    model_config = ConfigDict(strict=True)


class Request(RequestBase):
    id: int
    created_by: int
    status: str
    processed_by: int | None
    resolution_comment: str | None


class RequestUpdate(BaseModel):
    status: RequestStatus | None
    processed_by: int | None


class RequestCompleteReject(BaseModel):
    status: CompletedRejected


class OperatorBase(BaseModel):
    first_name: str
    last_name: str


class OperatorCreate(OperatorBase):
    pass


class Operator(OperatorBase):
    id: int
