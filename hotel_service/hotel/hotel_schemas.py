from datetime import date, datetime, time
from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from custom_object_id import ObjID

from ..apartment.apartment_schemas import ApartmentSchema


class AddressSchema(BaseModel):
    country: str = Field(max_length=255)
    city: str = Field(max_length=255)
    street: str = Field(max_length=255)
    house_number: Optional[str] = Field(None, max_length=10)
    longitude: float
    latitude: float


class CreateHotelSchema(BaseModel):
    is_pool: bool
    is_elevator: bool = True
    year_built: Optional[date]
    count_of_apartments: int = Field(..., gt=0)
    name: str
    description: Optional[str]
    address: AddressSchema

    @property
    def transformed_dict(self):
        _year_built = datetime.combine(
            date=self.year_built, time=time().min) if self.year_built else None
        return {
            'year_built': _year_built,
            **self.dict(exclude_none=True, exclude={'year_built'})
        }


class UpdateAddressSchema(AddressSchema):
    country: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    street: Optional[str] = Field(None, max_length=255)
    house_number: Optional[str] = Field(None, max_length=10)
    longitude: Optional[float]
    latitude: Optional[float]


class UpdateHotelSchema(BaseModel):
    is_pool: Optional[bool]
    is_elevator: Optional[bool]
    count_of_apartments: Optional[int] = Field(None, gt=0)
    name: Optional[str]
    description: Optional[str]
    address: Optional[UpdateAddressSchema]

    @property
    def transformed_dict(self):
        data = self.dict(exclude_none=True)
        if date_built := self.dict().get('year_built'):
            _d = datetime.combine(date_built, time().min)
            data.update({'year_built': _d})
        return data


class HotelSchema(CreateHotelSchema):
    id: ObjID = Field(alias='_id')
    address: AddressSchema
    account_id: str
    avg_rating: float = 0.0
    available_count_of_apartments: int

    apartments: Optional[list[ApartmentSchema]]

    class Config:
        json_encoders = {
            ObjID: lambda o: str(o),
            date: lambda d: d.strftime('%Y-%m-%d')
        }


class QueryHotelSchema(BaseModel):
    is_pool: Optional[bool]
    is_elevator: Optional[bool]
    from_year_built: Optional[date]
    to_year_built: Optional[date]
    avg_rating: Optional[float]
    country: Optional[str]
    city: Optional[str]
    street: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]

    @classmethod
    def query(cls, is_pool: Optional[bool] = Query(None),
              is_elevator: Optional[bool] = Query(None),
              avg_rating: Optional[float] = Query(None),
              from_year_built: Optional[date] = Query(None),
              to_year_built: Optional[date] = Query(None),
              longitude: Optional[float] = Query(None),
              latitude: Optional[float] = Query(None),
              country: Optional[str] = Query(None),
              city: Optional[str] = Query(None),
              street: Optional[str] = Query(None)):
        return cls(
            is_pool=is_pool, is_elevator=is_elevator, avg_rating=avg_rating,
            from_year_built=from_year_built, to_year_built=to_year_built,
            longitude=longitude, latitude=latitude, country=country, city=city,
            street=street
        )
