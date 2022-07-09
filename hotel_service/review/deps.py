from fastapi import Depends

from account.token_service import TokenService
from database import hotel_database
from permissions import AccountPermission
from token_service_data import token_service_data
from .review_repositories import ReviewRepositories

review_collection = hotel_database.review


async def get_review_collection(): yield review_collection


async def get_account(account=Depends(
    AccountPermission(
        token_service=TokenService(**token_service_data)).get_current_user
)):
    yield account


async def get_service_data(_review_collection=Depends(get_review_collection)):
    yield {
        'repository': ReviewRepositories(review_collection=_review_collection)
    }
