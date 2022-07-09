from datetime import date, datetime, time
from typing import Optional

from hotel_service.hotel.hotel_schemas import QueryHotelSchema
from common_compare_fields import CompareFieldsMixin


class QueryService(CompareFieldsMixin):

    @staticmethod
    def __query_avg_rating(avg_rating: Optional[float]):
        return {'avg_rating': {'$gte': avg_rating,
                               '$lte': 5.0}} if avg_rating else {}

    @staticmethod
    def __query_address(latitude: Optional[float], longitude: Optional[float],
                        country: Optional[str], city: Optional[str],
                        street: Optional[str]):
        if not latitude or longitude:
            geo_data = [('country', country), ('city', city),
                        ('street', street)]
            return {f'address.{var}': value for var, value in geo_data if value}

    @staticmethod
    def transform_date(_date: Optional[date] = None):
        if _date:
            return datetime.combine(_date, time().min)

    def prepare_query_data(self, query_data: QueryHotelSchema):
        return {
            **query_data.dict(exclude_none=True,
                              include={'is_pool', 'is_elevator'}),
            **self.__query_avg_rating(avg_rating=query_data.avg_rating),
            **self.__query_address(
                latitude=query_data.latitude, longitude=query_data.latitude,
                country=query_data.country,
                city=query_data.city, street=query_data.street),
            **self.compare('year_built',
                           self.transform_date(query_data.from_year_built),
                           self.transform_date(query_data.to_year_built))
        }
