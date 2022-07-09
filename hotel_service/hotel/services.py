from .hotel_schemas import CreateHotelSchema, HotelSchema, QueryHotelSchema, \
    UpdateHotelSchema
from .interfaces.hotel_repositories_interface import HotelRepositoriesInterface


class HotelServices:
    def __init__(self, repository: HotelRepositoriesInterface):
        self.__repository = repository

    async def create_hotel(self, hotel: CreateHotelSchema,
                           account) -> HotelSchema:
        return await self.__repository.create_hotel(hotel=hotel,
                                                    account=account)

    async def remove_hotel(self, hotel_id: str, account):
        return await self.__repository.remove_hotel(hotel_id=hotel_id,
                                                    account=account)

    async def update_hotel(self, hotel_id: str, account,
                           hotel: UpdateHotelSchema) -> HotelSchema:
        return await self.__repository \
            .update_hotel(hotel_id=hotel_id, account=account, hotel=hotel)

    async def show_detail_hotel(self, hotel_id: str) -> HotelSchema:
        return await self.__repository.show_detail_hotel(hotel_id=hotel_id)

    async def show_hotels(self, query_data: QueryHotelSchema,
                          limit: int = 20, skip: int = 0) -> list[HotelSchema]:
        return await self.__repository.show_hotels(limit=limit, skip=skip,
                                                   query_data=query_data)
