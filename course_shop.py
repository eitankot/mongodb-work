import json
from pymongo import MongoClient
from typing import Set, Any


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
        Test function which gets all the brands names.
        :return : Set of the different brands.
        """
        all_products = list(self.collection.find())
        different_brands = set(product["brand"] for product in all_products)
        return different_brands

    def fix_price(self, product_category: str, key: str, value: Any) -> None:
        query = {"categories": product_category}
        new_values = {"$set": {key: value}}
        self.collection.update_many(query, new_values)

    def update_max_to_min(self, product_category: str, key: str) -> None:
        min_doc_value = self.collection.find_one({"categories": product_category}, sort=[(key, 1)])[key]
        max_doc = self.collection.find_one({"categories": product_category}, sort=[(key, -1)])
        max_update = {"$set": {key: min_doc_value}}
        self.collection.update_one(max_doc, max_update)

    def change_value_for_all(self, value_name: str, difference: int):
        change_update = {"$inc": {value_name: difference}}
        for product in self.collection.find():
            self.collection.update_one(product, change_update)
