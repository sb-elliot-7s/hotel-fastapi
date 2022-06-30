import datetime
from bson import ObjectId
from .interfaces.favorite__repositories_interface import FavoriteRepositoriesInterface
from common_exceptions import raise_exception
from fastapi import status


class FavoriteRepositories(FavoriteRepositoriesInterface):
    def __init__(self, favorite_collection):
        self._favorite_collection = favorite_collection

    async def __get_favorite(self, favorite_id: str):
        favorite_filter = {'_id': ObjectId(favorite_id)}
        if (favorite := await self._favorite_collection.find_one(filter=favorite_filter)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, f'Favorite {favorite_id} not found')
        return favorite

    async def show_all_favorites(self, account, limit: int, skip: int):
        cursor = self._favorite_collection \
            .find({'account_id': account.id}) \
            .sort('datetime_added', -1) \
            .skip(skip) \
            .limit(limit)
        return [fav async for fav in cursor]

    async def add_to_fav(self, apartment_id: str, account):
        favorite_filter = {'account_id': account.id, 'apartment_id': apartment_id, 'is_favorite': True}
        if await self._favorite_collection.find_one(favorite_filter):
            raise_exception(status.HTTP_400_BAD_REQUEST, 'The apartment has already been added to favorites')
        document = {
            'account_id': account.id,
            'apartment_id': apartment_id,
            'is_favorite': True,
            'datetime_added': datetime.datetime.utcnow(),
        }
        result = await self._favorite_collection.insert_one(document=document)
        return await self.__get_favorite(favorite_id=result.inserted_id)

    async def remove_from_fav(self, favorite_id: str, account):
        fav_filter = {'_id': ObjectId(favorite_id), 'account_id': account.id, 'is_favorite': True}
        if (fav := await self._favorite_collection.find_one_and_delete(filter=fav_filter)) is None:
            raise_exception(status.HTTP_404_NOT_FOUND, f'Favorite {favorite_id} not found')
        return fav
