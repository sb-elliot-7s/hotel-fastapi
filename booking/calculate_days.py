from datetime import datetime


class CalculateDays:
    @staticmethod
    async def calculate(check_in: datetime, check_out: datetime):
        return (check_out - check_in).days

    # @staticmethod
    # async def __calculate_months(check_in: datetime, check_out: datetime):
    #     return (check_out.year - check_in.year) \
    #            * 12 + \
    #            (check_out.month - check_in.month)
