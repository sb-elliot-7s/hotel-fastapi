import json
import uuid
from datetime import datetime

from fastapi import HTTPException, status
from stripe import Charge, Customer

from configs import get_configs
from .interfaces.payment_repositories_interface import PaymentRepositoriesInterface
from .payment_schemas import CreatePaymentSchema, CardSchema
from common_aggregation_mixin import AggregationMixin
from .decorators import stripe_decorator_error
from .constants import PaymentStatus

from producer import producer


class PaymentRepositories(AggregationMixin, PaymentRepositoriesInterface):

    def __init__(self, payment_collection):
        self.__payment_collection = payment_collection

    @stripe_decorator_error
    async def create_payment(self, booking_id: str, account, payment_data: CreatePaymentSchema):
        charge = Charge.create(
            api_key=get_configs().stripe_api_key,
            amount=payment_data.amount,
            customer=account.stripe_account_id,
            source=payment_data.source,
            currency=payment_data.currency,
            description=payment_data.description,
            receipt_email=account.email,
            idempotency_key=str(uuid.uuid4())
        )
        am = str(payment_data.amount)[:-2] + '.' + str(payment_data.amount)[-2:]
        document = {
            'payment_id': charge['id'],
            'amount': am,
            'currency': payment_data.currency,
            'description': payment_data.description,
            'apartment_id': payment_data.apartment_id,
            'account_id': 'account.id',
            'created': datetime.utcnow(),
            'updated': None,
            'payment_status': PaymentStatus.PAID.value
        }
        await self.__payment_collection.insert_one(document=document)
        await producer.send_and_wait(
            topic='update-booking-payment-status',
            value=json.dumps(
                {
                    'booking_id': booking_id,
                    'payment_status': PaymentStatus.PAID.value
                }
            ).encode('utf-8')
        )
        return charge

    @stripe_decorator_error
    async def get_payment(self, account, payment_id: str):
        charge = Charge.retrieve(
            id=payment_id, api_key=get_configs().stripe_api_key
        )
        if charge['customer'] != account.stripe_account_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stripe account id don't equal account id"
            )
        return charge

    @stripe_decorator_error
    async def list_of_all_payments(self, account, limit: int = 10) -> dict:
        return Charge.list(
            api_key=get_configs().stripe_api_key,
            customer=account.stripe_account_id,
            limit=limit,
        )

    @stripe_decorator_error
    async def create_card(self, account, card_token: CardSchema):
        return Customer.create_source(
            api_key=get_configs().stripe_api_key,
            id=account.stripe_account_id,
            source=card_token.token
        )
