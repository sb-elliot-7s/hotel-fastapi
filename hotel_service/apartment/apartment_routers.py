from fastapi import APIRouter, Depends, status

apartment_router = APIRouter(prefix='/apartment', tags=['apartment'])

"""
создать апартаменты
удалить апт
обновить апт
показать детально апт
показать все доступные апартаменты в отеле / фильтр
"""


@apartment_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_apartment():
    pass


@apartment_router.delete('/{apartment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_apartment(apartment_id: str):
    pass


@apartment_router.patch('/{apartment_id}', status_code=status.HTTP_200_OK)
async def update_apartment(apartment_id: str):
    pass


@apartment_router.get('/{apartment_id}', status_code=status.HTTP_200_OK)
async def detail_apartment(apartment_id: str):
    pass


@apartment_router.get('/hotel/{hotel_id}', status_code=status.HTTP_200_OK)
async def all_available_apartments_in_the_hotel(hotel_id: str, limit: int = 20, skip: int = 0):
    pass
