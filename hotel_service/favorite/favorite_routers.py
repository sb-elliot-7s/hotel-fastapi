from fastapi import APIRouter, Depends, status, responses
from .services import FavoriteServices
from .favorite_schemas import FavoriteSchema
from .deps import get_service_data, get_account

favorite_router = APIRouter(prefix='/favorite', tags=['favorite'])


@favorite_router.get('/', status_code=status.HTTP_200_OK,
                     response_model=list[FavoriteSchema],
                     response_model_by_alias=False)
async def show_all_favorites(limit: int = 5, skip: int = 0,
                             service=Depends(get_service_data),
                             account=Depends(get_account)):
    return await FavoriteServices(**service) \
        .show_all_favorites(account=account, limit=limit, skip=skip)


@favorite_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED,
                      response_model=FavoriteSchema,
                      response_model_by_alias=False)
async def add_to_fav(apartment_id: str, service=Depends(get_service_data),
                     account=Depends(get_account)):
    return await FavoriteServices(**service) \
        .add_to_fav(apartment_id=apartment_id, account=account)


@favorite_router.delete('/{favorite_id}',
                        status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_fav(favorite_id: str, service=Depends(get_service_data),
                          account=Depends(get_account)):
    if not (_ := await FavoriteServices(
            **service
    ).remove_from_fav(favorite_id=favorite_id, account=account)):
        return responses.JSONResponse({'detail': 'Favorite obj not deleted'})
    return responses.JSONResponse(
        {'detail': f'Favorite obj {favorite_id} has been deleted'}
    )
