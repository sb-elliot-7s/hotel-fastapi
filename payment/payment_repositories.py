from stripe import Charge, error
from configs import get_configs
from .interfaces.payment_repositories_interface import PaymentRepositoriesInterface
from .payment_schemas import CreatePaymentSchema, QueryPaymentSchema
from common_aggregation_mixin import AggregationMixin


def stripe_decorator_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught

            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)
        except error.RateLimitError as e:
            # Too many requests made to the API too quickly
            pass
        except error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            pass
        except error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except error.APIConnectionError as e:
            # Network communication with Stripe failed
            pass
        except error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            pass

    return wrapper


class PaymentRepositories(AggregationMixin, PaymentRepositoriesInterface):

    def __init__(self, payment_collection, booking_collection):
        self.__booking_collection = booking_collection
        self.__payment_collection = payment_collection

    @stripe_decorator_error
    async def create_payment(self, account, payment_data: CreatePaymentSchema):
        return Charge.create(
            api_key=get_configs().stripe_api_key,
            amount=payment_data.amount,
            currency=payment_data.currency,
            source="tok_visa",
            description=payment_data.description,
        )

    async def cancel_payment(self, account, payment_id: str):
        ...

    async def get_payment(self, account, payment_id: str):
        charge = Charge.retrieve(
            id=payment_id,
            api_key=get_configs().stripe_api_key
        )

    async def get_payments(self, account, limit: int, skip: int,
                           query_payment_data: QueryPaymentSchema):
        ...
