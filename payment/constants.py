from enum import Enum


class PaymentMode(Enum):
    PAYMENT = 'payment'
    SUBSCRIPTION = 'subscription'
    SETUP = 'setup'


class PaymentStatus(Enum):
    PAID = 'paid'
    UNPAID = 'unpaid'
    IN_PROCESS = 'in_process'
    CANCELED = 'canceled'
