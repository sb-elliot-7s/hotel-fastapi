from fastapi import APIRouter, Depends, status, responses
from .favorite_repositories import FavoriteRepositories
from .services import FavoriteServices
from permissions import AccountPermission
from account.token_service import TokenService
from token_service_data import token_service_data
from .deps import get_favorite_collection
from .favorite_schemas import FavoriteSchema

favorite_router = APIRouter(prefix='/favorite', tags=['favorite'])


@favorite_router.get('/', status_code=status.HTTP_200_OK, response_model=list[FavoriteSchema],
                     response_model_by_alias=False)
async def show_all_favorites(limit: int = 5, skip: int = 0,
                             favorite_collection=Depends(get_favorite_collection),
                             account=Depends(AccountPermission(token_service=TokenService(
                                 **token_service_data)).get_current_user)):
    return await FavoriteServices(repository=FavoriteRepositories(favorite_collection=favorite_collection)) \
        .show_all_favorites(account=account, limit=limit, skip=skip)


@favorite_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED, response_model=FavoriteSchema,
                      response_model_by_alias=False)
async def add_to_fav(apartment_id: str, favorite_collection=Depends(get_favorite_collection),
                     account=Depends(AccountPermission(
                         token_service=TokenService(**token_service_data)).get_current_user)):
    return await FavoriteServices(repository=FavoriteRepositories(favorite_collection=favorite_collection)) \
        .add_to_fav(apartment_id=apartment_id, account=account)


@favorite_router.delete('/{favorite_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_fav(favorite_id: str, favorite_collection=Depends(get_favorite_collection),
                          account=Depends(AccountPermission(
                              token_service=TokenService(**token_service_data)).get_current_user)):
    if not (_ := await FavoriteServices(
            repository=FavoriteRepositories(favorite_collection=favorite_collection)
    ).remove_from_fav(favorite_id=favorite_id, account=account)):
        return responses.JSONResponse({'detail': 'Favorite obj not deleted'})
    return responses.JSONResponse({'detail': f'Favorite obj {favorite_id} has been deleted'})
