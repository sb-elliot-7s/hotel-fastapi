from fastapi import APIRouter, status, Depends, responses
from .hotel_schemas import CreateHotelSchema, QueryHotelSchema, HotelSchema, \
    UpdateHotelSchema
from .services import HotelServices
from .deps import get_service_data, get_account

hotel_routers = APIRouter(prefix='/hotel', tags=['hotel'])


@hotel_routers.post('/', status_code=status.HTTP_201_CREATED,
                    response_model=HotelSchema,
                    response_model_by_alias=False)
async def create_hotel(hotel: CreateHotelSchema,
                       account=Depends(get_account),
                       service=Depends(get_service_data)):
    return await HotelServices(**service) \
        .create_hotel(hotel=hotel, account=account)


@hotel_routers.delete('/{hotel_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_hotel(hotel_id: str,
                       account=Depends(get_account),
                       service=Depends(get_service_data)):
    if not (_ := await HotelServices(**service)
            .remove_hotel(hotel_id=hotel_id, account=account)):
        return responses.JSONResponse({'detail': 'Hotel not deleted'})
    return responses.JSONResponse(
        {'detail': f'Hotel {hotel_id} has been deleted'}
    )


@hotel_routers.patch('/{hotel_id}', status_code=status.HTTP_200_OK,
                     response_model=HotelSchema,
                     response_model_by_alias=False)
async def update_hotel(hotel_id: str, hotel: UpdateHotelSchema,
                       account=Depends(get_account),
                       service=Depends(get_service_data)):
    return await HotelServices(**service) \
        .update_hotel(hotel_id=hotel_id, account=account, hotel=hotel)


@hotel_routers.get('/{hotel_id}', status_code=status.HTTP_200_OK,
                   response_model=HotelSchema,
                   response_model_by_alias=False)
async def show_detail_hotel(hotel_id: str, service=Depends(get_service_data)):
    return await HotelServices(**service) \
        .show_detail_hotel(hotel_id=hotel_id)


@hotel_routers.get('/', status_code=status.HTTP_200_OK,
                   response_model=list[HotelSchema],
                   response_model_by_alias=False)
async def show_hotels(
        limit: int = 20, skip: int = 0,
        query_data: QueryHotelSchema = Depends(QueryHotelSchema.query),
        service=Depends(get_service_data)
):
    return await HotelServices(**service) \
        .show_hotels(limit=limit, skip=skip, query_data=query_data)
