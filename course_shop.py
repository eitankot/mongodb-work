import json

import pymongo.command_cursor
from pymongo import MongoClient
from typing import Set, Any, List, Tuple, Iterator


class ProductsManager:
    def __init__(self, db_name: str, collection_name: str) -> None:
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_json_to_collection(self, json_path: str) -> None:
        """
        insert json data into the collection of the mongodb

        :param json_path: json file path to add to the collection
        """
        inventory_collection = self.collection
        with open(json_path) as products_file:
            json_file_data = json.load(products_file)
        inventory_collection.insert_many(json_file_data)

    def count_sizes(self) -> pymongo.command_cursor.CommandCursor:
        """
        Counts the total amount of each size, no matter which category.
        :return: Iterator contains dictionaries, which have size id and total amount.
        """
        pipeline = [
            {"$unwind": "$sizes"},
            {"$group": {"_id": "$sizes.size", "total": {"$sum": "$sizes.amount"}}}
        ]
        return self.collection.aggregate(pipeline)
