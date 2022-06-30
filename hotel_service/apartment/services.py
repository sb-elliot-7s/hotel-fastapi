from .apartment_schemas import CreateApartmentSchema, ApartmentSchema, ApartmentQuerySchema, \
    UpdateApartmentSchema
from .interfaces.apartment_repositories_interface import ApartmentRepositoriesInterface


class ApartmentServices:
    def __init__(self, repository: ApartmentRepositoriesInterface):
        self.__repository = repository

    async def create_apartment(self, account, hotel_station,
                               apartment: CreateApartmentSchema) -> ApartmentSchema:
        return await self.__repository. \
            create_apartment(account=account, hotel_station=hotel_station, apartment=apartment)

    async def remove_apartment(self, account, apartment_id: str):
        return await self.__repository. \
            remove_apartment(account=account, apartment_id=apartment_id)

    async def update_apartment(self, account, apartment_id: str,
                               apartment: UpdateApartmentSchema) -> ApartmentSchema:
        return await self.__repository. \
            update_apartment(account=account, apartment_id=apartment_id, apartment=apartment)

    async def detail_apartment(self, apartment_id: str) -> ApartmentSchema:
        return await self.__repository. \
            detail_apartment(apartment_id=apartment_id)

    async def all_available_apartments(self, hotel_id: str, query_data: ApartmentQuerySchema,
                                       limit: int = 20, skip: int = 0) -> list[ApartmentSchema]:
        return await self.__repository. \
            all_available_apartments(hotel_id=hotel_id, limit=limit, skip=skip, query_data=query_data)
