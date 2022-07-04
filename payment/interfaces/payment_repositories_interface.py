from abc import ABC, abstractmethod
from ..payment_schemas import CreatePaymentSchema, QueryPaymentSchema


class PaymentRepositoriesInterface(ABC):
    @abstractmethod
    async def create_payment(self, account, payment_data: CreatePaymentSchema): pass

    @abstractmethod
    async def cancel_payment(self, account, payment_id: str): pass

    @abstractmethod
    async def get_payment(self, account, payment_id: str): pass

    @abstractmethod
    async def get_payments(self, account, limit: int,
                           skip: int, query_payment_data: QueryPaymentSchema): pass
