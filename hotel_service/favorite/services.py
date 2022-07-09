from .interfaces.favorite__repositories_interface import \
    FavoriteRepositoriesInterface


class FavoriteServices:
    def __init__(self, repository: FavoriteRepositoriesInterface):
        self.__repository = repository

    async def show_all_favorites(self, account, limit: int, skip: int):
        return await self.__repository. \
            show_all_favorites(account=account, limit=limit, skip=skip)

    async def add_to_fav(self, apartment_id: str, account):
        return await self.__repository.add_to_fav(apartment_id=apartment_id,
                                                  account=account)

    async def remove_from_fav(self, favorite_id: str, account):
        return await self.__repository.remove_from_fav(favorite_id=favorite_id,
                                                       account=account)
