from abc import ABC, abstractmethod

from ..payment_schemas import CreatePaymentSchema, CardSchema, UpdateCardSchema


class PaymentRepositoriesInterface(ABC):
    @abstractmethod
    async def create_payment(
            self, account, booking_id: str, payment_data: CreatePaymentSchema):
        pass

    @abstractmethod
    async def get_payment(self, account, payment_id: str): pass

    @abstractmethod
    async def list_of_all_payments(self, account, limit: int = 10) -> dict:
        pass

    @abstractmethod
    async def create_card(self, account, card_token: CardSchema): pass

    @staticmethod
    @abstractmethod
    async def get_card(account, card_id: str): pass

    @staticmethod
    @abstractmethod
    async def delete_card(card_id: str, account): pass

    @staticmethod
    @abstractmethod
    async def list_of_all_cards(account, limit: int = 10): pass

    @abstractmethod
    async def update_card(self, account, card_id: str,
                          updated_card_data: UpdateCardSchema):
        pass
