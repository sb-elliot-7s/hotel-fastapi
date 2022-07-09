from common_compare_fields import CompareFieldsMixin
from .payment_schemas import QueryPaymentSchema


class PaymentQueryService(CompareFieldsMixin):
    def query_filter(self, query_data: QueryPaymentSchema):
        price_filter = self.compare(
            field='amount',
            from_value=query_data.from_amount,
            to_value=query_data.to_amount
        )
        """
            currency: Optional[str]
            from_amount: Optional[float]
            to_amount: Optional[float]
            payment_status: Optional[PaymentStatus]
        """
        return {
            **query_data.dict(
                exclude_none=True,
                include={
                    'currency', 'payment_status'
                }
            ),
            **price_filter
        }
