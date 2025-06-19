import json
from pymongo import MongoClient
from typing import Set


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

    def get_brand_names(self) -> Set[str]:
        """
        gets all the brand name

        :return : set of different brands
        """
        return set(self.collection.distinct("brands"))
