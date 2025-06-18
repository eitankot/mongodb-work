import json
from pymongo import MongoClient
from typing import Set, Any
from bson.son import SON

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

    def count_all_products_by_color(self) -> Any :
        """
        count all the products by color
        :return: Cursor of all products with the sum
        """
        pipeline = [
                {"$unwind": "$color"},
                {"$group": {"_id": "$color", "count": {"$sum": "$amount"}}},
                {"$sort": SON([("count", -1), ("_id", -1)])},
        ]
        return self.collection.aggregate(pipeline)

    def change_sales(self) -> Any:
        pipeline = [
            {"match": {"$brand": "Castro"}},
            {"$set": {"$price": {"$multiply": ["$price", 0.9]}}},
        ]
        return self.collection.aggregate(pipeline)