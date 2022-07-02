from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from custom_object_id import ObjID
from datetime import datetime


class PaymentStatus(Enum):
    PAID = 'paid'
    UNPAID = 'unpaid'
    IN_PROCESS = 'in_process'
    CANCELED = 'canceled'


class CreateBookingSchema(BaseModel):
    check_in: datetime
    check_out: datetime


class BookingSchema(CreateBookingSchema):
    id: ObjID = Field(alias='_id')
    apartment_id: str
    account_id: str
    count_of_days_rent: int
    month_price: float
    day_price: float
    total_money: float
    payment_status: PaymentStatus
    is_active: bool
    updated: Optional[datetime]

    class Config:
        json_encoders = {
            ObjID: lambda x: str(x),
            datetime: lambda d: d.strftime('%Y-%d-%m %H:%S')
        }
