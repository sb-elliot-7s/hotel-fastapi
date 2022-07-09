from typing import Optional

from fastapi import UploadFile

from .apartment_schemas import CreateApartmentSchema, ApartmentSchema, \
    ApartmentQuerySchema, \
    UpdateApartmentSchema, SearchApartmentSchema
from .interfaces.apartment_repositories_interface import \
    ApartmentRepositoriesInterface


class ApartmentServices:
    def __init__(self, repository: ApartmentRepositoriesInterface):
        self.__repository = repository

    async def create_apartment(self, account, apartment: CreateApartmentSchema,
                               images: Optional[
                                   list[UploadFile]] = None) -> ApartmentSchema:
        return await self.__repository. \
            create_apartment(account=account, apartment=apartment,
                             images=images)

    async def remove_apartment(self, account, apartment_id: str):
        return await self.__repository. \
            remove_apartment(account=account, apartment_id=apartment_id)

    async def update_apartment(self, account, apartment_id: str,
                               apartment: UpdateApartmentSchema,
                               images: Optional[
                                   list[UploadFile]] = None) -> ApartmentSchema:
        return await self.__repository. \
            update_apartment(account=account, apartment_id=apartment_id,
                             apartment=apartment, images=images)

    async def detail_apartment(self, apartment_id: str) -> ApartmentSchema:
        return await self.__repository. \
            detail_apartment(apartment_id=apartment_id)

    async def all_available_apartments(
            self, hotel_id: str,
            query_data: ApartmentQuerySchema,
            limit: int = 20, skip: int = 0
    ) -> list[ApartmentSchema]:
        return await self.__repository. \
            all_available_apartments(hotel_id=hotel_id, limit=limit, skip=skip,
                                     query_data=query_data)

    async def search_apartment(self, search_data: SearchApartmentSchema,
                               skip: int, limit: int):
        return await self.__repository.search(search_data=search_data,
                                              skip=skip, limit=limit)

    async def delete_image(self, image_id: str, account):
        return await self.__repository.delete_image(image_id=image_id,
                                                    account=account)
