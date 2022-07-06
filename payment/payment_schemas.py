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


description_card_fields = {
    'address_city': 'City/District/Suburb/Town/Village.',
    'address_country': 'Billing address country, if provided when creating card.',
    'address_line1': 'Address line 1 (Street address/PO Box/Company name).',
    'address_line2': 'Address line 2 (Apartment/Suite/Unit/Building).',
    'address_state': 'State/County/Province/Region.',
    'address_zip': 'ZIP or postal code.',
    'exp_month': 'Two digit number representing the card’s expiration month.',
    'exp_year': 'Four digit number representing the card’s expiration year.',
    'metadata': 'Set of key-value pairs that you can attach to an object. '
                'This can be useful for storing additional information about '
                'the object in a structured format. Individual keys can be unset '
                'by posting an empty value to them. All keys can be unset by posting'
                ' an empty value to metadata.',
    'name': 'Cardholder name.'
}


class UpdateCardSchema(BaseModel):
    address_city: Optional[str] = Field(
        description=description_card_fields.get('address_city'))
    address_country: Optional[str] = Field(
        description=description_card_fields.get('address_country'))
    address_line1: Optional[str] = Field(
        description=description_card_fields.get('address_line1'))
    address_line2: Optional[str] = Field(
        description=description_card_fields.get('address_line2'))
    address_state: Optional[str] = Field(
        description=description_card_fields.get('address_state'))
    address_zip: Optional[str] = Field(
        description=description_card_fields.get('address_zip'))
    exp_month: Optional[int] = Field(
        description=description_card_fields.get('exp_month'))
    exp_year: Optional[int] = Field(
        description=description_card_fields.get('exp_year'))
    metadata: Optional[dict] = Field(
        description=description_card_fields.get('metadata'))
    name: Optional[str] = Field(description=description_card_fields.get('name'))
