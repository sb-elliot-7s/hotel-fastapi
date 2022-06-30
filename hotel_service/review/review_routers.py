from fastapi import APIRouter, Depends, status, responses
from permissions import AccountPermission
from account.token_service import TokenService
from .review_schemas import CreateReviewSchema, ReviewSchema
from token_service_data import token_service_data
from .services import ReviewServices
from .review_repositories import ReviewRepositories
from .deps import get_review_collection

review_router = APIRouter(prefix='/review', tags=['review'])


@review_router.post('/{apartment_id}', status_code=status.HTTP_201_CREATED, response_model=ReviewSchema,
                    response_model_by_alias=False)
async def write_review(apartment_id: str, review: CreateReviewSchema,
                       review_collection=Depends(get_review_collection),
                       account=Depends(AccountPermission(
                           token_service=TokenService(**token_service_data)).get_current_user)):
    return await ReviewServices(repository=ReviewRepositories(review_collection=review_collection)) \
        .write_review(apartment_id=apartment_id, account=account, review=review)


@review_router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_review(review_id: str, review_collection=Depends(get_review_collection),
                        account=Depends(AccountPermission(
                            token_service=TokenService(**token_service_data)).get_current_user)):
    if not (_ := await ReviewServices(repository=ReviewRepositories(review_collection=review_collection))
            .remove_review(review_id=review_id, account=account)):
        return responses.JSONResponse({'detail': 'Review not deleted'})
    return responses.JSONResponse({'detail': f'Review {review_id} has been deleted'})


@review_router.patch('/{review_id}', status_code=status.HTTP_200_OK, response_model=ReviewSchema,
                     response_model_by_alias=False)
async def update_review(
        review_id: str, review: CreateReviewSchema,
        review_collection=Depends(get_review_collection),
        account=Depends(
            AccountPermission(token_service=TokenService(**token_service_data)).get_current_user)):
    return await ReviewServices(repository=ReviewRepositories(review_collection=review_collection)) \
        .update_review(review_id=review_id, account=account, review=review)


@review_router.get('/{apartment_id}', status_code=status.HTTP_200_OK, response_model=list[ReviewSchema],
                   response_model_by_alias=False)
async def show_reviews_to_apartment(apartment_id: str, limit: int = 20, skip: int = 0,
                                    review_collection=Depends(get_review_collection)):
    return await ReviewServices(repository=ReviewRepositories(review_collection=review_collection)) \
        .get_reviews(apartment_id=apartment_id, limit=limit, skip=skip)
