class CompareFieldsMixin:
    @staticmethod
    def compare(field: str, from_value=None, to_value=None):
        both = {field: {'$gte': from_value, '$lte': to_value}}
        only_left = {field: {'$gte': from_value}}
        only_right = {field: {'$lte': to_value}}

        return both if from_value and to_value \
            else only_left if from_value \
            else only_right if to_value \
            else {}
