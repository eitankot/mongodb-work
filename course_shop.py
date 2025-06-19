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

    def get_brand_names(self) -> Set[str]:
        """
        gets all the brand name

        :return : set of different brands
        """
        all_products = list(self.collection.find())
        different_brands = set(product["brand"] for product in all_products)
        return different_brands

    def get_all_categories(self) -> Set[str]:
        """
        get all the categories
        :return: set of all categories
        """
        return set(self.collection.distinct("categories"))

    def get_all_shirts_colors(self) -> Set[str]:
        """
        get all the shirts colors
        :return: a set of all shirts colors
        """
        return set(self.collection.distinct("color", {"categories": "shirts"}))

    def count_all_products_by_color(self) -> Any :
        """
        count all the products by color
        :return: Cursor of all products with the sum
        """
        pipeline = [
                {"$group": {"_id": "$color", "count": {"$sum": "$amount"}}},
                {"$sort": {("count", -1), ("_id", -1)}},
        ]
        return self.collection.aggregate(pipeline)