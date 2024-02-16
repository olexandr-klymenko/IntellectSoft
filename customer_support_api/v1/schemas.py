import phonenumbers
from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from customer_support_api.models import RequestStateEnum


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
    phone: str


class CustomerCreate(CustomerBase):
    phone: Annotated[str, BeforeValidator(phone_number_validator)]


class CustomerGet(CustomerBase):
    is_deleted: bool


class CustomerUpdate(CustomerCreate):
    first_name: str | None = None
    last_name: str | None = None
    phone: Annotated[
        str, BeforeValidator(phone_number_validator)
    ] | None = None
    is_deleted: bool | None = None


class RequestBase(BaseModel):
    body: str


class RequestCreate(RequestBase):
    model_config = ConfigDict(strict=True)


class RequestGet(RequestBase):
    created_by: int
    status: str
    processed_by: int
    resolution_comment: str


class RequestUpdate(BaseModel):
    body: str | None
    status: RequestStateEnum | None
    processed_by: int | None
    resolution_comment: str | None
