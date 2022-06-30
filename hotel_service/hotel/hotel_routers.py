from fastapi import APIRouter, status, Depends, responses
from .hotel_schemas import CreateHotelSchema, QueryHotelSchema, HotelSchema, UpdateHotelSchema
from .hotel_repositories import HotelRepositories
from .services import HotelServices
from .deps import get_hotel_collection
from permissions import AccountPermission
from account.token_service import TokenService
from token_service_data import token_service_data

hotel_routers = APIRouter(prefix='/hotel', tags=['hotel'])


@hotel_routers.post('/', status_code=status.HTTP_201_CREATED, response_model=HotelSchema,
                    response_model_by_alias=False)
async def create_hotel(hotel: CreateHotelSchema,
                       account=Depends(AccountPermission(
                           token_service=TokenService(**token_service_data)).get_owner_user),
                       hotel_collection=Depends(get_hotel_collection)):
    return await HotelServices(repository=HotelRepositories(hotel_collection=hotel_collection)) \
        .create_hotel(hotel=hotel, account=account)


@hotel_routers.delete('/{hotel_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_hotel(hotel_id: str,
                       account=Depends(AccountPermission(token_service=TokenService(
                           **token_service_data)).get_owner_user),
                       hotel_collection=Depends(get_hotel_collection)):
    if not (_ := await HotelServices(repository=HotelRepositories(hotel_collection=hotel_collection))
            .remove_hotel(hotel_id=hotel_id, account=account)):
        return responses.JSONResponse({'detail': 'Hotel not deleted'})
    return responses.JSONResponse({'detail': f'Hotel {hotel_id} has been deleted'})


@hotel_routers.patch('/{hotel_id}', status_code=status.HTTP_200_OK, response_model=HotelSchema,
                     response_model_by_alias=False)
async def update_hotel(hotel_id: str, hotel: UpdateHotelSchema,
                       account=Depends(AccountPermission(token_service=TokenService(
                           **token_service_data)).get_owner_user),
                       hotel_collection=Depends(get_hotel_collection)):
    return await HotelServices(repository=HotelRepositories(hotel_collection=hotel_collection)) \
        .update_hotel(hotel_id=hotel_id, account=account, hotel=hotel)


@hotel_routers.get('/{hotel_id}', status_code=status.HTTP_200_OK, response_model=HotelSchema,
                   response_model_by_alias=False)
async def show_detail_hotel(hotel_id: str, hotel_collection=Depends(get_hotel_collection)):
    return await HotelServices(repository=HotelRepositories(hotel_collection=hotel_collection)) \
        .show_detail_hotel(hotel_id=hotel_id)


@hotel_routers.get('/', status_code=status.HTTP_200_OK, response_model=list[HotelSchema],
                   response_model_by_alias=False)
async def show_hotels(limit: int = 20, skip: int = 0,
                      query_data: QueryHotelSchema = Depends(QueryHotelSchema.query),
                      hotel_collection=Depends(get_hotel_collection)):
    return await HotelServices(repository=HotelRepositories(hotel_collection=hotel_collection)) \
        .show_hotels(limit=limit, skip=skip, query_data=query_data)
