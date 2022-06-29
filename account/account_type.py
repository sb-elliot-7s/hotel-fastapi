from enum import Enum


class AccountType(Enum):
    SUPERUSER = 'super_user'
    AGENT = 'agent'
    CUSTOMER = 'customer'
