import json
from pymongo import MongoClient
from course_shop import ProductsManager

DB_NAME = "Products"
COLLECTION_NAME = "Inventory"

def create_collection() -> ProductsManager:
    products_manager = ProductsManager(DB_NAME, COLLECTION_NAME)
    return products_manager

def main():
    products_manager = create_collection()
    products_manager.client.drop_database(DB_NAME)
    products_manager.insert_json_to_collection("products.json")
    print("The brands we have are:")
    print(products_manager.get_brand_names())


if __name__ == '__main__':
    main()