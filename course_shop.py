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

    def set_fixed_price(self, product_category: str, key: str, value: Any) -> None:
        """
        Sets a fixed value of all keys for a specific category.
        :param product_category: The category to change.
        :param key: The key to find and update per each product of the category.
        :param value: The value to set to all the keys.
        """
        query = {"categories": product_category}
        new_values = {"$set": {key: value}}
        self.collection.update_many(query, new_values)

    def update_max_to_min(self, product_category: str, key: str) -> None:
        """
        Sets the minimum value of a key in a category to the maximum value of a key in the same category.
        :param product_category: The category to swap in.
        :param key: The key to swap between the two products.
        """
        min_doc_value = self.collection.find_one({"categories": product_category}, sort=[(key, 1)])[key]
        max_doc = self.collection.find_one({"categories": product_category}, sort=[(key, -1)])
        max_update = {"$set": {key: min_doc_value}}
        self.collection.update_one(max_doc, max_update)

    def change_value_for_all(self, key: str, difference: int) -> None:
        """
        Updates the value to all the products in the collection.
        :param key: The key to add or sub from. Must hold a numeric value.
        :param difference: The amount to add or sub.
        """
        change_update = {"$inc": {key: difference}}
        self.collection.update_many({}, change_update)
