from stripe import error
from fastapi import HTTPException, status


def stripe_decorator_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=e.user_message
            )
            # print('Status is: %s' % e.http_status)
            # print('Code is: %s' % e.code)
            # # param is '' in this case
            # print('Param is: %s' % e.param)
            # print('Message is: %s' % e.user_message)
        except error.RateLimitError as e:
            print(e)
            # Too many requests made to the API too quickly
            pass
        except error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            pass
        except error.AuthenticationError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Not validate api key'
            )
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except error.APIConnectionError as e:
            print(e)
            # Network communication with Stripe failed
            pass
        except error.StripeError as e:
            print(e)
            # Display a very generic error to the user, and maybe send
            # yourself an email
            pass
        except Exception as e:
            print(e)
            # Something else happened, completely unrelated to Stripe
            pass

    return wrapper
