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

    def change_sales(self) -> Any:
        pipeline = [
            {
                "$facet": {
                    "CastroSales":[
                        {"$match": {"brand": "Castro"}},
                        {"$set": {"price": {"$multiply": ["$price", 0.9]}}}
                    ],
                    "RenuarSales": [
                        {"$match": {"brand": "Renuar"}},
                        {"$set": {"price": {"$multiply": ["$price", 0.7]}}}
                    ],
                    "CourseShopSales": [
                        {"$match": {"brand": "CourseShop"}},
                        {"$set": {"price": {"$multiply": ["$price", 0.5]}}}
                    ],
                    "ZaraSales": [
                        {"$match": {"brand": "Zara"}},
                        {"$set": {"price": {"$multiply": ["$price", 0.8]}}}
                    ],
                    "FoxSales": [
                        {"$match": {"brand": "Fox"}},
                        {"$set": {"price": {"$multiply": ["$price", 0.6]}}}
                    ]
                }
            }

        ]
        return self.collection.aggregate(pipeline)