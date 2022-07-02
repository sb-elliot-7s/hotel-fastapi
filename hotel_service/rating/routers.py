from fastapi import Depends, APIRouter, status

from account.token_service import TokenService
from permissions import AccountPermission
from token_service_data import token_service_data
from .schemas import RateApartmentSchema, RatingSchema
from .deps import get_rating_collection
from .repositories import RatingRepositories
from .services import RatingService

rating_router = APIRouter(prefix='/rating', tags=['ratings'])


async def get_customer_account(
        account=Depends(AccountPermission(token_service=TokenService(**token_service_data)).get_current_user)
):
    yield account


@rating_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED,
                    response_model=RatingSchema, response_model_by_alias=False)
async def rate_apartment(apartment_id: str, rate_apartment_data: RateApartmentSchema,
                         account=Depends(get_customer_account),
                         rating_collection=Depends(get_rating_collection)):
    return await RatingService(repository=RatingRepositories(rating_collection=rating_collection)) \
        .rate_apartment(apartment_id=apartment_id, account=account, rate_data=rate_apartment_data)


@rating_router.patch('/{rating_id}', status_code=status.HTTP_200_OK,
                     response_model=RatingSchema, response_model_by_alias=False)
async def change_rating(rating_id: str, rate_apartment_data: RateApartmentSchema,
                        account=Depends(get_customer_account),
                        rating_collection=Depends(get_rating_collection)):
    return await RatingService(repository=RatingRepositories(rating_collection=rating_collection)) \
        .change_rating(rating_id=rating_id, account=account, rate_apartment_data=rate_apartment_data)
