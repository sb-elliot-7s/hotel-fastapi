from fastapi import APIRouter, status, Depends
from .refund_services import RefundService
from .refund_repositories import RefundRepositories
from .refund_schema import CreateRefundSchema
from account.deps import get_account_collection
from .deps import get_payment_collection

refund_router = APIRouter(prefix='/refund', tags=['refund'])


@refund_router.post('/{charge_id}', status_code=status.HTTP_201_CREATED)
async def refund_money(
        charge_id: str, refund_data: CreateRefundSchema,
        payment_collection=Depends(get_payment_collection),
        account=Depends(get_account_collection)
):
    return await RefundService(
        repository=RefundRepositories(payment_collection=payment_collection)
    ).refund_money(
        charge_id=charge_id, refund_data=refund_data, account=account)


@refund_router.get('/{refund_id}', status_code=status.HTTP_200_OK)
async def retrieve_refund(
        refund_id: str, payment_collection=Depends(get_payment_collection),
        account=Depends(get_account_collection)
):
    return await RefundService(
        repository=RefundRepositories(payment_collection=payment_collection)
    ).retrieve_refund(refund_id=refund_id, account=account)


@refund_router.get('/', status_code=status.HTTP_200_OK)
async def list_of_all_refunds(
        charge_id: str, limit: int = 10,
        account=Depends(get_account_collection),
        payment_collection=Depends(get_payment_collection)
) -> dict:
    return await RefundService(
        repository=RefundRepositories(payment_collection=payment_collection)
    ).list_of_all_refunds(charge_id=charge_id, limit=limit, account=account)
