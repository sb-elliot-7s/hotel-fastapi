from abc import ABC, abstractmethod

from payment.refund_schema import CreateRefundSchema


class RefundRepositoriesInterface(ABC):
    @abstractmethod
    async def refund_money(self, account, charge_id: str,
                           refund_data: CreateRefundSchema):
        pass

    @abstractmethod
    async def retrieve_refund(self, account, refund_id: str): pass

    @abstractmethod
    async def list_of_all_refunds(
            self, account, charge_id: str, limit: int = 10) -> dict:
        pass
