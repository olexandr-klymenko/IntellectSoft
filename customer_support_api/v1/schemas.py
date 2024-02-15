import phonenumbers
from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


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


class CustomerUpdate(CustomerCreate):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class RequestBase(BaseModel):
    created_by: int
    body: str


class RequestCreate(RequestBase):
    pass


class RequestGet(RequestBase):
    status: str
    processed_by: int
    resolution_comment: str
