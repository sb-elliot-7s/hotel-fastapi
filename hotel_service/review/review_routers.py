from fastapi import APIRouter, Depends, status, responses
from .review_schemas import CreateReviewSchema, ReviewSchema
from .services import ReviewServices
from .deps import get_service_data, get_account

review_router = APIRouter(prefix='/review', tags=['review'])


@review_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED,
                    response_model=ReviewSchema,
                    response_model_by_alias=False)
async def write_review(apartment_id: str, review: CreateReviewSchema,
                       service=Depends(get_service_data),
                       account=Depends(get_account)):
    return await ReviewServices(**service).write_review(
        apartment_id=apartment_id, account=account, review=review)


@review_router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_review(review_id: str,
                        service=Depends(get_service_data),
                        account=Depends(get_account)):
    if not (_ := await ReviewServices(**service)
            .remove_review(review_id=review_id, account=account)):
        return responses.JSONResponse({'detail': 'Review not deleted'})
    return responses.JSONResponse(
        {'detail': f'Review {review_id} has been deleted'}
    )


@review_router.patch('/{review_id}', status_code=status.HTTP_200_OK,
                     response_model=ReviewSchema,
                     response_model_by_alias=False)
async def update_review(
        review_id: str, review: CreateReviewSchema,
        service=Depends(get_service_data),
        account=Depends(get_account)):
    return await ReviewServices(**service) \
        .update_review(review_id=review_id, account=account, review=review)


@review_router.get('/{apartment_id}', status_code=status.HTTP_200_OK,
                   response_model=list[ReviewSchema],
                   response_model_by_alias=False)
async def show_reviews_to_apartment(apartment_id: str,
                                    limit: int = 20, skip: int = 0,
                                    service=Depends(get_service_data)):
    return await ReviewServices(**service) \
        .get_reviews(apartment_id=apartment_id, limit=limit, skip=skip)
