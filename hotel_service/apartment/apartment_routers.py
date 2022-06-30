from fastapi import APIRouter, Depends, status, responses
from .services import ApartmentServices
from .apartment_repositories import ApartmentRepositories
from permissions import AccountPermission
from account.token_service import TokenService
from token_service_data import token_service_data
from .deps import get_apartment_collection
from .apartment_schemas import CreateApartmentSchema, ApartmentQuerySchema, ApartmentSchema, \
    UpdateApartmentSchema
from ..hotel.deps import get_hotel_collection

apartment_router = APIRouter(prefix='/apartment', tags=['apartment'])


async def get_repository(apartment_collection=Depends(get_apartment_collection)):
    yield {
        'repository': ApartmentRepositories(apartment_collection=apartment_collection)
    }


async def get_account(
        account=Depends(AccountPermission(token_service=TokenService(**token_service_data)).get_owner_user)
):
    yield account


@apartment_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ApartmentSchema,
                       response_model_by_alias=False)
async def create_apartment(apartment: CreateApartmentSchema, repo=Depends(get_repository),
                           account=Depends(get_account), hotel_collection=Depends(get_hotel_collection)):
    return await ApartmentServices(**repo) \
        .create_apartment(apartment=apartment, hotel_station=hotel_collection, account=account)


@apartment_router.delete('/{apartment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_apartment(apartment_id: str, repository=Depends(get_repository),
                           account=Depends(get_account)):
    if not (_ := await ApartmentServices(**repository)
            .remove_apartment(apartment_id=apartment_id, account=account)):
        return responses.JSONResponse({'detail': 'Apartment not deleted'})
    return responses.JSONResponse({'detail': f'Apartment {apartment_id} has been deleted'})


@apartment_router.patch('/{apartment_id}', status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def update_apartment(apartment_id: str, apartment: UpdateApartmentSchema,
                           repository=Depends(get_repository), account=Depends(get_account)):
    return await ApartmentServices(**repository) \
        .update_apartment(apartment_id=apartment_id, account=account, apartment=apartment)


@apartment_router.get('/{apartment_id}', status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def detail_apartment(apartment_id: str, repository=Depends(get_repository)):
    return await ApartmentServices(**repository).detail_apartment(apartment_id=apartment_id)


@apartment_router.get('/hotel_service/{hotel_id}', response_model=list[ApartmentSchema],
                      status_code=status.HTTP_200_OK, response_model_by_alias=False)
async def all_available_apartments_in_the_hotel(
        hotel_id: str, repository=Depends(get_repository), limit: int = 20, skip: int = 0,
        query_data: ApartmentQuerySchema = Depends(ApartmentQuerySchema.query)):
    return await ApartmentServices(**repository) \
        .all_available_apartments(hotel_id=hotel_id, query_data=query_data, limit=limit, skip=skip)
