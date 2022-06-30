from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from custom_object_id import ObjID


class CreateReviewSchema(BaseModel):
    review: str


class ReviewSchema(CreateReviewSchema):
    id: ObjID = Field(alias='_id')
    account_id: str
    apartment_id: str
    date_posted: datetime
    date_updated: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y-%m-%d %H:%M'),
            ObjID: lambda o: str(o)
        }
