from typing import Optional

from hotel_service.apartment.apartment_schemas import ApartmentQuerySchema
from common_compare_fields import CompareFieldsMixin


class ApartmentQueryService(CompareFieldsMixin):
    def prepare_query_data(self, data: ApartmentQuerySchema):
        price_filter = self.compare(
            field='price', from_value=data.min_price, to_value=data.max_price)
        area_filter = self.compare(
            field='total_area',
            from_value=data.min_area,
            to_value=data.max_area
        )
        bedrooms = self.__find_rooms(field='numer_of_bedrooms',
                                     rooms=data.list_number_of_bedrooms)
        bathrooms = self.__find_rooms(field='number_of_bathroom',
                                      rooms=data.list_number_of_bathroom)
        return {
            'is_active': True,
            'is_booked': False,
            **price_filter,
            **area_filter,
            **bedrooms,
            **bathrooms,
            **data.dict(exclude_none=True,
                        include={'is_furnished', 'is_garage'})
        }

    @staticmethod
    def __find_rooms(field: str, rooms: Optional[list] = None):
        return {field: {'$in': rooms}} if rooms else {}
