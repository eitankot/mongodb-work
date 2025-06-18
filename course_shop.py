import json
from pymongo import MongoClient
from typing import Set


class ProductsManager:
    def __init__(self, db_name: str, collection_name: str) -> None:
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_json_to_collection(self,json_data) -> None:
        """
        insert json data into the collection of the mongodb

        :param json_data: json data to add to the collection
        """
        inventory_collection = self.collection
        inventory_collection.insert_many(json_data)

    def get_brand_names(self) -> Set[str]:
        """
        gets all the brand name

        :return : set of different brands
        """
        all_products = list(self.collection.find())
        different_brands = set(product["brand"] for product in all_products)
        return different_brands

    def get_all_categories(self) -> Set[str]:
        return set(self.collection.distinct("categories"))

    def get_all_shirts_colors(self) -> Set[str]:
        return set(self.collection.distinct("colors", {"categories": "shirts"}))