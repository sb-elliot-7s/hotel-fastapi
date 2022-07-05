from .interfaces.payment_repositories_interface import PaymentRepositoriesInterface
from .payment_schemas import CreatePaymentSchema, CardSchema


class PaymentService:
    def __init__(self, repository: PaymentRepositoriesInterface):
        self.__repository = repository

    async def create_payment(self, booking_id: str, account, payment_data: CreatePaymentSchema):
        return await self.__repository \
            .create_payment(booking_id=booking_id, payment_data=payment_data, account=account)

    async def get_payment(self, payment_id: str, account):
        return await self.__repository \
            .get_payment(payment_id=payment_id, account=account)

    async def get_payments(self, account, limit: int = 10):
        return await self.__repository \
            .list_of_all_payments(account=account, limit=limit)

    async def create_card(self, account, card_token: CardSchema):
        return await self.__repository \
            .create_card(account=account, card_token=card_token)
