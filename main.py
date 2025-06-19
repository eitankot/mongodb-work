from __future__ import annotations
import json
from pymongo import MongoClient
from course_shop import ProductsManager
from typing import List, Any

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


def find_all_shirts(products_manager: ProductsManager) -> List[Any]:
    """
    finds all shirt and prints the shirts
    """
    print("getting all shirts:")
    all_shirts_cursor = products_manager.collection.find({ "categories": "shirts"})
    print(list(all_shirts_cursor))
    return list(all_shirts_cursor)


def find_three_products(products_manager: ProductsManager) -> List[Any]:
    """
    finds and prints three products
    """
    print("getting three products")
    list_three_products = list(products_manager.collection.find(limit=3))
    print(f"!!!!!!!!!\n{list_three_products}\n!!!!!!!\n")
    return list_three_products


def find_cheaper_than_min_price(products_manager: ProductsManager, min_price: int) -> List[Any]:
    """
    finds and prints all the products cheaper than 30
    """
    print(f"getting all products with prices lower than {min_price}:")
    list_products_cheaper_than_30 = list(products_manager.collection.find({'price': {'$lt': min_price}}))
    print(f"!!!!!!!!!\n{list_products_cheaper_than_30}\n!!!!!!!\n")
    return list_products_cheaper_than_30


def find_pants_in_price_range(products_manager: ProductsManager, min_price: int, max_price: int) -> List[Any]:
    """
    finds and prints all the pants in price range
    """
    print(f"prints all the pants cheaper with {min_price} < price < {max_price}")
    list_pants_in_price_range = list(products_manager.collection.find({
        'categories': 'pants','price': {'$lt': max_price, '$gt': min_price}
        }))
    print(f"!!!!!!!!!\n{list_pants_in_price_range}\n!!!!!!!\n")
    return list_pants_in_price_range

def find_ties_and_suits(products_manager: ProductsManager) -> List[Any]:
    """
    finds and prints all ties and suits
    """
    print("prints all the ties and suits")
    list_pants_in_price_range = list(products_manager.collection.find({'categories': 'suits'}, {'categories': 'ties'}))
    print(f"!!!!!!!!!\n{list_pants_in_price_range}\n!!!!!!!\n")
    return list_pants_in_price_range



def amount_of_products(products_manager: ProductsManager) -> int:
    """
    returns the amount of products
    """
    print("prints amount of products in the store")
    count_products = products_manager.collection.count_documents({})
    print(f"!!!!!!!!!\n{count_products}\n!!!!!!!\n")
    return count_products


def main():
    products_manager = create_collection()
    products_manager.client.drop_database(DB_NAME)
    products_manager.insert_json_to_collection("products.json")
    find_all_shirts(products_manager)
    find_three_products(products_manager)
    find_cheaper_than_min_price(products_manager, 30)
    find_pants_in_price_range(products_manager, 80, 150)
    find_ties_and_suits(products_manager)
    amount_of_products(products_manager)


if __name__ == '__main__':
    main()