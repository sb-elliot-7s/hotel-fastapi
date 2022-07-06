from fastapi import APIRouter, status, Depends
from .payment_services import PaymentService
from .payment_repositories import PaymentRepositories
from permissions import AccountPermission
from payment.payment_schemas import CreatePaymentSchema, CardSchema, \
    UpdateCardSchema
from account.token_service import TokenService
from token_service_data import token_service_data
from .deps import get_payment_collection

payment_router = APIRouter(prefix='/payment', tags=['payment'])


async def get_account(
        account=Depends(
            AccountPermission(
                token_service=TokenService(**token_service_data)
            ).get_current_user
        )
): yield account


async def get_repository_service(
        payment_collection=Depends(get_payment_collection)
):
    yield {
        'repository': PaymentRepositories(payment_collection=payment_collection)
    }


@payment_router.post('/card', status_code=status.HTTP_201_CREATED)
async def create_card(
        card_token=Depends(CardSchema),
        account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    """
    card_token: A token, like the ones returned by Stripe.js.
        Stripe will automatically validate the card.
        more: "https://stripe.com/docs/api/cards/create"
    """
    return await PaymentService(**repository_service) \
        .create_card(account=account, card_token=card_token)


@payment_router.get('/card/', status_code=status.HTTP_200_OK)
async def list_of_all_cards(
        account=Depends(get_account), limit: int = 10,
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .list_of_all_cards(account=account, limit=limit)


@payment_router.get('/card/{card_id}', status_code=status.HTTP_200_OK)
async def get_card(card_id: str, account=Depends(get_account),
                   repository_service=Depends(get_repository_service)):
    return await PaymentService(**repository_service) \
        .get_card(account=account, card_id=card_id)


@payment_router.patch('/card/{card_id}', status_code=status.HTTP_200_OK)
async def update_card(
        card_id: str, updated_card_data: UpdateCardSchema,
        account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service).update_card(
        card_id=card_id, account=account, updated_card_data=updated_card_data)


@payment_router.delete('/card/{card_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(card_id: str, account=Depends(get_account),
                      repository_service=Depends(get_repository_service)):
    return await PaymentService(**repository_service) \
        .delete_card(account=account, card_id=card_id)


@payment_router.get('/all', status_code=status.HTTP_200_OK)
async def get_payments(
        limit: int = 20,
        account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .get_payments(account=account, limit=limit)


@payment_router.post('/{booking_id}', status_code=status.HTTP_201_CREATED)
async def create_payment(
        booking_id: str,
        payment_data: CreatePaymentSchema,
        account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service).create_payment(
        booking_id=booking_id, payment_data=payment_data, account=account)


@payment_router.get('/{payment_id}', status_code=status.HTTP_200_OK)
async def get_payment(
        payment_id: str,
        account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .get_payment(payment_id=payment_id, account=account)
