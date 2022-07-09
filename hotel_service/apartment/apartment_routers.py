from typing import Optional

from fastapi import APIRouter, Depends, status, responses, UploadFile, File
from .services import ApartmentServices
from .apartment_repositories import ApartmentRepositories
from permissions import AccountPermission
from account.token_service import TokenService
from token_service_data import token_service_data
from .deps import get_apartment_collection, hotel_database
from .apartment_schemas import CreateApartmentSchema, ApartmentQuerySchema, \
    ApartmentSchema, \
    UpdateApartmentSchema, SearchApartmentSchema
from image_service.image_service import ImageService
from ..hotel.deps import get_hotel_collection

apartment_router = APIRouter(prefix='/apartment', tags=['apartment'])


async def get_repository(
        apartment_collection=Depends(get_apartment_collection),
        hotel_collection=Depends(get_hotel_collection)
):
    yield {
        'repository': ApartmentRepositories(
            apartment_collection=apartment_collection,
            hotel_collection=hotel_collection,
            image_service=ImageService(database=hotel_database)
        )
    }


async def get_owner_account(
        account=Depends(AccountPermission(
            token_service=TokenService(**token_service_data)).get_owner_user)
):
    yield account


@apartment_router.get('/search_apartments', status_code=status.HTTP_200_OK,
                      response_model=list[ApartmentSchema],
                      response_model_by_alias=False)
async def search_apartment(
        skip: int = 0, limit: int = 20,
        search_data: SearchApartmentSchema = Depends(
            SearchApartmentSchema.as_query
        ),
        repository=Depends(get_repository)
):
    return await ApartmentServices(**repository) \
        .search_apartment(search_data=search_data, skip=skip, limit=limit)


@apartment_router.post('/', status_code=status.HTTP_201_CREATED,
                       response_model=ApartmentSchema,
                       response_model_by_alias=False)
async def create_apartment(
        apartment: CreateApartmentSchema = Depends(
            CreateApartmentSchema.as_form),
        images: Optional[list[UploadFile]] = File(None),
        repo=Depends(get_repository), account=Depends(get_owner_account)
):
    return await ApartmentServices(**repo) \
        .create_apartment(apartment=apartment, images=images, account=account)


@apartment_router.delete('/{apartment_id}',
                         status_code=status.HTTP_204_NO_CONTENT)
async def remove_apartment(
        apartment_id: str, repository=Depends(get_repository),
        account=Depends(get_owner_account)
):
    if not (_ := await ApartmentServices(**repository)
            .remove_apartment(apartment_id=apartment_id, account=account)):
        return responses.JSONResponse({'detail': 'Apartment not deleted'})
    return responses. \
        JSONResponse({'detail': f'Apartment {apartment_id} has been deleted'})


@apartment_router.patch('/{apartment_id}', status_code=status.HTTP_200_OK,
                        response_model=ApartmentSchema,
                        response_model_by_alias=False)
async def update_apartment(
        apartment_id: str,
        apartment: UpdateApartmentSchema = Depends(
            UpdateApartmentSchema.as_form),
        repository=Depends(get_repository), account=Depends(get_owner_account),
        images: Optional[list[UploadFile]] = File(None)
):
    return await ApartmentServices(**repository) \
        .update_apartment(apartment_id=apartment_id,
                          account=account,
                          apartment=apartment,
                          images=images)


@apartment_router.get('/{apartment_id}', status_code=status.HTTP_200_OK,
                      response_model=ApartmentSchema,
                      response_model_by_alias=False)
async def detail_apartment(apartment_id: str,
                           repository=Depends(get_repository)):
    return await ApartmentServices(**repository) \
        .detail_apartment(apartment_id=apartment_id)


@apartment_router.get('/hotel_service/{hotel_id}',
                      response_model=list[ApartmentSchema],
                      status_code=status.HTTP_200_OK,
                      response_model_by_alias=False)
async def all_available_apartments_in_the_hotel(
        hotel_id: str, repository=Depends(get_repository),
        limit: int = 40, skip: int = 0,
        query_data: ApartmentQuerySchema = Depends(ApartmentQuerySchema.query)
):
    return await ApartmentServices(**repository) \
        .all_available_apartments(hotel_id=hotel_id,
                                  query_data=query_data,
                                  limit=limit, skip=skip)


@apartment_router.delete('/images/{image_id}')
async def delete_image(image_id: str, account=Depends(get_owner_account),
                       repository=Depends(get_repository)):
    await ApartmentServices(**repository) \
        .delete_image(image_id=image_id, account=account)
    return responses.JSONResponse(
        {'detail': f'Image {image_id} has been deleted'})
