import json
from pymongo import MongoClient
from typing import Set

class ProductsManager:
    def __init__(self) -> None:
        self.client = MongoClient('127.0.0.1', 27017)

    def insert_json_to_collection(self, db_name: str, collection_name: str, json_data) -> None:
        """
        insert json data into the collection of the mongodb

        :param db_name: database name
        :param collection_name: collection name
        :param json_data: json data to add to the collection
        """
        products_db = self.client[db_name]
        inventory_collection = products_db[collection_name]
        inventory_collection.insert_many(json_data)

    def get_brand_names(self, db_name: str, collection_name: str) -> Set[str]:
        """
        gets all the brand name

        :param db_name: database name
        :param collection_name: collection name
        :return : set of different brands
        """
        collection = self.client[db_name][collection_name]
        all_products = list(collection.find())
        different_brands = set(product["brand"] for product in all_products)
        return different_brands