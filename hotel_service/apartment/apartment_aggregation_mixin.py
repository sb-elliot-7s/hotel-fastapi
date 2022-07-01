class AggregationMixin:

    @staticmethod
    def lookup(secondary_collection: str, secondary_collection_field: str,
               primary_collection_field: str, _as: str):
        return {
            '$lookup': {
                'from': secondary_collection,
                'localField': primary_collection_field,
                'foreignField': secondary_collection_field,
                'as': _as
            }
        }

    @staticmethod
    def search_text(text: str): return {'$text': {'$search': text}}

    @staticmethod
    def match(query: dict): return {'$match': query}

    @staticmethod
    def sort(**values): return {'$sort': values}

    @staticmethod
    def skip(value: int): return {'$skip': value}

    @staticmethod
    def limit(value: int): return {'$limit': value}

    @staticmethod
    def add_fields(new_name: str, operator: str, old_name: str):
        return {"$addFields": {new_name: {f"${operator}": f"${old_name}"}}}
