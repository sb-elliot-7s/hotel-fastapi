from datetime import datetime

from pydantic import BaseModel, Field

from custom_object_id import ObjID


class RateApartmentSchema(BaseModel):
    grade: int = Field(..., ge=0, le=5)


class RatingSchema(RateApartmentSchema):
    id: ObjID = Field(alias='_id')
    account_id: str
    apartment_id: str
    created: datetime

    class Config:
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M'),
            ObjID: lambda o: str(o)
        }
