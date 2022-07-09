from datetime import datetime, date, time
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from custom_object_id import ObjID

from .account_type import AccountType


class BaseAccountSchema(BaseModel):
    email: EmailStr
    phone: int
    first_name: Optional[str]
    last_name: Optional[str]
    date_birth: Optional[date]
    account_type: AccountType
    is_superuser: bool = False
    is_agent: bool = False


class CreateAccountSchema(BaseAccountSchema):
    password: str

    @property
    def transform_dict(self):
        _date_birth = datetime.combine(
            self.date_birth, time().min) if self.date_birth else None
        return {
            **self.dict(exclude_none=True, exclude={
                'password', 'date_birth', 'account_type'
            }),
            'date_birth': _date_birth,
            'account_type': self.account_type.value
        }


class AccountSchema(BaseAccountSchema):
    id: ObjID = Field(alias='_id')
    profile_image: Optional[str]
    is_active: bool
    stripe_account_id: Optional[str]
    created: datetime
    updated: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda value: value.strftime('%Y-%m-%d %H:%M'),
            ObjID: lambda value: str(value)
        }


class TokenSchema(BaseModel):
    token: str
