from fastapi import Depends, APIRouter, status
from .schemas import RateApartmentSchema, RatingSchema
from .services import RatingService
from .deps import get_service_data, get_customer_account

rating_router = APIRouter(prefix='/rating', tags=['ratings'])


@rating_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED,
                    response_model=RatingSchema, response_model_by_alias=False)
async def rate_apartment(
        apartment_id: str, rate_apartment_data: RateApartmentSchema,
        account=Depends(get_customer_account),
        service=Depends(get_service_data)
):
    return await RatingService(**service).rate_apartment(
        apartment_id=apartment_id, account=account,
        rate_data=rate_apartment_data
    )


@rating_router.patch('/{rating_id}', status_code=status.HTTP_200_OK,
                     response_model=RatingSchema,
                     response_model_by_alias=False)
async def change_rating(
        rating_id: str, rate_apartment_data: RateApartmentSchema,
        account=Depends(get_customer_account),
        service=Depends(get_service_data)
):
    return await RatingService(**service).change_rating(
        rating_id=rating_id, account=account,
        rate_apartment_data=rate_apartment_data
    )
