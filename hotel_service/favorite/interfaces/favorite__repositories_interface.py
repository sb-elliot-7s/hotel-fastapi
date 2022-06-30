from abc import ABC, abstractmethod


class FavoriteRepositoriesInterface(ABC):
    @abstractmethod
    async def show_all_favorites(self, account, limit: int, skip: int):
        pass

    @abstractmethod
    async def add_to_fav(self, apartment_id: str, account):
        pass

    @abstractmethod
    async def remove_from_fav(self, favorite_id: str, account):
        pass
