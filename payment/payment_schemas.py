from datetime import datetime
from typing import Optional
from .constants import PaymentStatus
from pydantic import BaseModel, Field

from custom_object_id import ObjID
from fastapi import Query


class CreatePaymentSchema(BaseModel):
    amount: int = Field(..., gt=0)
    currency: Optional[str] = 'usd'
    description: Optional[str]
    apartment_id: str
    source: Optional[str]


class PaymentSchema(CreatePaymentSchema):
    id: ObjID = Field(alias='_id')
    account_id: str
    created: datetime
    updated: Optional[datetime]
    payment_status: PaymentStatus

    class Config:
        json_encoders = {
            datetime: lambda d: d.strftimr('%Y-%m-%d %H:%M'),
            ObjID: lambda o: str(o)
        }


class QueryPaymentSchema(BaseModel):
    currency: Optional[str]
    from_amount: Optional[float]
    to_amount: Optional[float]
    payment_status: Optional[PaymentStatus]

    @classmethod
    def as_query(
            cls, currency: Optional[str] = Query(None),
            from_amount: Optional[float] = Query(None),
            to_amount: Optional[float] = Query(None),
            payment_status: Optional[PaymentStatus] = Query(None)
    ):
        return cls(currency=currency, from_amount=from_amount,
                   to_amount=to_amount, payment_status=payment_status)


class CardSchema(BaseModel):
    token: str
