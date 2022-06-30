from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from custom_object_id import ObjID
from fastapi import Query


class CreateApartmentSchema(BaseModel):
    hotel_id: str
    total_area: float
    numer_of_bedrooms: int = 1
    number_of_bathroom: int = 1
    is_booked: bool = False
    price: float
    title: str
    description: Optional[str]
    is_furnished: bool = True
    is_garage: bool = False
    is_active: bool = True


class UpdateApartmentSchema(BaseModel):
    total_area: Optional[float]
    numer_of_bedrooms: Optional[int]
    number_of_bathroom: Optional[int]
    is_booked: Optional[bool]
    price: Optional[float]
    title: Optional[str]
    description: Optional[str]
    is_furnished: Optional[bool]
    is_garage: Optional[bool]
    is_active: Optional[bool]

    @property
    def transformed_dict(self):
        return {**self.dict(exclude_none=True), 'updated': datetime.utcnow()}


class ApartmentSchema(CreateApartmentSchema):
    id: ObjID = Field(alias='_id')
    account_id: str
    created: datetime
    updated: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y-%m-%d %H:%M'),
            ObjID: lambda o: str(o)
        }


class ApartmentQuerySchema(BaseModel):
    min_area: Optional[float]
    max_area: Optional[float]
    list_number_of_bedrooms: Optional[list[int]]
    list_number_of_bathroom: Optional[list[int]]
    min_price: Optional[float]
    max_price: Optional[float]
    is_furnished: Optional[bool]
    is_garage: Optional[bool]

    @classmethod
    def query(cls, is_furnished: Optional[bool] = Query(None),
              is_garage: Optional[bool] = Query(None),
              min_area: Optional[float] = Query(None),
              max_area: Optional[float] = Query(None),
              min_price: Optional[float] = Query(None),
              max_price: Optional[float] = Query(None),
              list_number_of_bedrooms: Optional[list[int]] = Query(None),
              list_number_of_bathroom: Optional[list[int]] = Query(None)):
        return cls(
            is_furnished=is_furnished,
            is_garage=is_garage,
            min_area=min_area,
            max_area=max_area,
            min_price=min_price,
            max_price=max_price,
            list_number_of_bathroom=list_number_of_bathroom,
            list_number_of_bedrooms=list_number_of_bedrooms
        )


class Image(BaseModel):
    id: ObjID = Field(alias='_id')
    apartment_id: str

    class Config:
        json_encoders = {ObjID: lambda o: str(o)}
