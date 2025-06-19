from __future__ import annotations
import json
from pymongo import MongoClient
from course_shop import ProductsManager

DB_NAME = "Products"
COLLECTION_NAME = "Inventory"

def create_collection() -> ProductsManager:
    products_manager = ProductsManager(DB_NAME, COLLECTION_NAME)
    return products_manager

def find_one_product(products_manager: ProductsManager) -> None:
    print("a random hat in the db:")
    print(products_manager.collection.find_one({"categories": "hats"}))
    print("a random shirt with a price of 25 in the db:")
    print(products_manager.collection.find_one({"categories": "shirts", "price": 25}))

def find_all_shirts(products_manager: ProductsManager) -> None:
    print("getting all shirts:")
    all_shirts_cursor = products_manager.collection.find({ "categories": "shirts"})
    print(list(all_shirts_cursor))

def find_products_by_query(products_manager: ProductsManager) -> None:
    print("getting three proucts")
    list_three_products = list(products_manager.collection.find(limit=3))
    print(f"!!!!!!!!!\n{list_three_products}\n!!!!!!!\n")
    print("getting all products with prices lower than 30:")
    list_products_cheaper_than_30 = list(products_manager.collection.find({'price': {'$lt': 30}}))
    print(f"!!!!!!!!!\n{list_products_cheaper_than_30}\n!!!!!!!\n")
    print("prints all the pants cheaper with 80 < price < 150")
    list_pants_in_price_range = list(products_manager.collection.find({'categories': 'pants','price': {'$lt': 150, '$gt': 80}}))
    print(f"!!!!!!!!!\n{list_pants_in_price_range}\n!!!!!!!\n")
    print("prints all the ties and suits")
    list_pants_in_price_range = list(products_manager.collection.find({'$or': [{'categories': 'suits'}, {'categories': 'ties'}]}))
    print(f"!!!!!!!!!\n{list_pants_in_price_range}\n!!!!!!!\n")
    print("prints amount of products in the store")
    count_products = products_manager.collection.count_documents({})
    print(f"!!!!!!!!!\n{count_products}\n!!!!!!!\n")



def main():
    products_manager = create_collection()
    products_manager.client.drop_database(DB_NAME)
    products_manager.client.drop_database("products.json")
    find_products_by_query(products_manager)





if __name__ == '__main__':
    main()