import uuid

from .interfaces.refund_service_interface import RefundRepositoriesInterface
from stripe import Refund
from configs import get_configs
from .decorators import stripe_decorator_error
from .refund_schema import CreateRefundSchema
from common_exceptions import raise_exception
from fastapi import status


class RefundRepositories(RefundRepositoriesInterface):

    def __init__(self, payment_collection):
        self.__payment_collection = payment_collection

    async def __get_payment(self, charge_id: str, account):
        return await self.__payment_collection.find_one(
            filter={
                'payment_id': charge_id, 'account_id': account.id
            }
        )

    @stripe_decorator_error
    async def refund_money(self, account, charge_id: str,
                           refund_data: CreateRefundSchema):
        if self.__get_payment(charge_id=charge_id, account=account):
            return Refund.create(
                api_key=get_configs().stripe_api_key,
                charge=charge_id,
                amount=refund_data.amount,
                reason=refund_data.reason,
                idempotency_key=str(uuid.uuid4())
            )

    @stripe_decorator_error
    async def retrieve_refund(self, account, refund_id: str):
        refund = Refund.retrieve(id=refund_id,
                                 api_key=get_configs().stripe_api_key)
        if not await self.__get_payment(
                charge_id=refund['charge'], account=account):
            raise_exception(status.HTTP_404_NOT_FOUND, 'Charge not found')
        return refund

    @stripe_decorator_error
    async def list_of_all_refunds(
            self, account, charge_id: str, limit: int = 10) -> dict:
        if await self.__get_payment(charge_id=charge_id, account=account):
            return Refund.list(
                api_key=get_configs().stripe_api_key,
                charge=charge_id,
                limit=limit,
            )
