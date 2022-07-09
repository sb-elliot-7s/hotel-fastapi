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


class ReasonRefund(Enum):
    DUPLICATE = 'duplicate'
    FRAUDULENT = 'fraudulent'
    REQUESTED_BY_CUSTOMER = 'requested_by_customer'


class RefundStatus(Enum):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    REQUIRES_ACTION = 'requires_action'
