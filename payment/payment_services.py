from .interfaces.payment_repositories_interface import PaymentRepositoriesInterface
from .payment_schemas import CreatePaymentSchema, QueryPaymentSchema


class PaymentService:
    def __init__(self, repository: PaymentRepositoriesInterface):
        self.__repository = repository

    async def create_payment(self, account, payment_data: CreatePaymentSchema):
        return await self.__repository \
            .create_payment(account=account, payment_data=payment_data)

    async def cancel_payment(self, account, payment_id: str):
        return await self.__repository \
            .cancel_payment(account=account, payment_id=payment_id)

    async def get_payment(self, account, payment_id: str):
        return await self.__repository \
            .get_payment(account=account, payment_id=payment_id)

    async def get_payments(self, account, limit: int, skip: int,
                           query_payment_data: QueryPaymentSchema):
        return await self.__repository.get_payments(
            account=account, skip=skip, limit=limit,
            query_payment_data=query_payment_data
        )
