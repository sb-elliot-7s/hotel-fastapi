from .interfaces.payment_repositories_interface import \
    PaymentRepositoriesInterface
from .payment_schemas import CreatePaymentSchema, CardSchema, UpdateCardSchema


class PaymentService:
    def __init__(self, repository: PaymentRepositoriesInterface):
        self.__repository = repository

    async def create_payment(self, booking_id: str, account,
                             payment_data: CreatePaymentSchema):
        return await self.__repository.create_payment(
            booking_id=booking_id, payment_data=payment_data, account=account)

    async def get_payment(self, payment_id: str, account):
        return await self.__repository \
            .get_payment(payment_id=payment_id, account=account)

    async def get_payments(self, account, limit: int = 10):
        return await self.__repository \
            .list_of_all_payments(account=account, limit=limit)

    async def create_card(self, account, card_token: CardSchema):
        return await self.__repository \
            .create_card(account=account, card_token=card_token)

    async def get_card(self, account, card_id: str):
        return await self.__repository \
            .get_card(account=account, card_id=card_id)

    async def delete_card(self, card_id: str, account):
        return await self.__repository \
            .delete_card(card_id=card_id, account=account)

    async def list_of_all_cards(self, account, limit: int = 10):
        return await self.__repository \
            .list_of_all_cards(account=account, limit=limit)

    async def update_card(self, card_id: str, account,
                          updated_card_data: UpdateCardSchema):
        return await self.update_card(
            card_id=card_id,
            account=account,
            updated_card_data=updated_card_data
        )
