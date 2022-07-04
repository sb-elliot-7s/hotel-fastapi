from fastapi import APIRouter, status, Depends
from .payment_services import PaymentService
from .payment_repositories import PaymentRepositories
from permissions import AccountPermission
from payment.payment_schemas import CreatePaymentSchema, QueryPaymentSchema
from account.token_service import TokenService
from token_service_data import token_service_data
from .deps import get_payment_collection
from booking.deps import get_booking_collection

payment_router = APIRouter(prefix='/payment', tags=['payment'])


async def get_account(account=Depends(
    AccountPermission(token_service=TokenService(**token_service_data)).get_current_user)
):
    yield account


async def get_repository_service(
        payment_collection=Depends(get_payment_collection),
        booking_collection=Depends(get_booking_collection)
):
    yield {
        'repository': PaymentRepositories(
            payment_collection=payment_collection, booking_collection=booking_collection
        )
    }


@payment_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_payment(
        payment_data: CreatePaymentSchema,
        account=Depends(get_account), repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .create_payment(account=account, payment_data=payment_data)


@payment_router.patch('/{payment_id}')
async def cancel_payment(
        payment_id: str, account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .cancel_payment(account=account, payment_id=payment_id)


@payment_router.get('/{payment_id}')
async def get_payment(
        payment_id: str, account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .get_payment(account=account, payment_id=payment_id)


@payment_router.get('/all')
async def get_payments(
        limit: int = 20, skip: int = 0,
        query_payment_data: QueryPaymentSchema = Depends(QueryPaymentSchema.as_query),
        account=Depends(get_account),
        repository_service=Depends(get_repository_service)
):
    return await PaymentService(**repository_service) \
        .get_payments(account=account, skip=skip, limit=limit,
                      query_payment_data=query_payment_data)
