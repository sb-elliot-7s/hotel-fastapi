from typing import Union, Optional

from bson import ObjectId


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
    def search_text(text: Optional[str]):
        return {'$text': {'$search': text or ''}}

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

    @staticmethod
    def filter_objects(**params): return params

    @staticmethod
    def pull_item(**conditions): return {'$pull': {**conditions}}

    @staticmethod
    def set_document(document: dict): return {'$set': document}

    @staticmethod
    def push_item_to_array(**field_and_items):
        return {'$push': {**field_and_items}}

    @staticmethod
    def push_items_to_array(array_name: str, items: list, default=None):
        return {'$push': {array_name: {'$each': items or default}}}

    @staticmethod
    def check_in(array_: list): return {'$in': array_}

    @staticmethod
    def expr_(condition: dict): return {'$expr': condition}

    @staticmethod
    def compare_values(operator: str, left_value, right_value):
        return {f'${operator}': [left_value, right_value]}

    @staticmethod
    def inc_value(**fields):
        """
        :param fields: key: str value: int
        :return: {'inc': {'key1': value1, 'key2': value2}
        """
        return {'$inc': {**fields}}

    @staticmethod
    def project(**specifications): return {'$project': specifications}

    @staticmethod
    def group_by(_id: Union[str, dict], **fields):
        return {'$group': {'_id': _id, **fields}}

    async def get_common_pipeline_for_find_apartments(
            self, skip: int, limit: int, _filter: dict):
        return [
            self.match(query=_filter),
            self.add_fields(
                new_name='apt_id', operator='toString', old_name='_id'),
            self.lookup(secondary_collection='review',
                        secondary_collection_field='apartment_id',
                        primary_collection_field='apt_id', _as='reviews'),
            self.skip(value=skip),
            self.limit(value=limit),
            self.sort(created=-1),
        ]

    async def get_pipeline_for_detail_apartment(self, apartment_id: str):
        return [
            self.match(query={'_id': ObjectId(apartment_id)}),
            self.add_fields(new_name='apt_id', operator='toString',
                            old_name='_id'),
            self.lookup('review', 'apartment_id', 'apt_id', 'reviews')
        ]
