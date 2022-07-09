from .interfaces.refund_service_interface import RefundRepositoriesInterface
from .refund_schema import CreateRefundSchema


class RefundService:
    def __init__(self, repository: RefundRepositoriesInterface):
        self.__repository = repository

    async def refund_money(self, account, charge_id: str,
                           refund_data: CreateRefundSchema):
        return await self.__repository.refund_money(
            account=account, charge_id=charge_id, refund_data=refund_data
        )

    async def retrieve_refund(self, account, refund_id: str):
        return await self.__repository \
            .retrieve_refund(refund_id=refund_id, account=account)

    async def list_of_all_refunds(
            self, account, charge_id: str, limit: int = 10) -> dict:
        return await self.__repository.list_of_all_refunds(
            charge_id=charge_id, limit=limit, account=account
        )
