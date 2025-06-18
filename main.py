import json
from pymongo import MongoClient
from course_shop import ProductsManager
import pprint

DB_NAME = "Products"
COLLECTION_NAME = "Inventory"

def create_collection() -> ProductsManager:
    products_manager = ProductsManager(DB_NAME, COLLECTION_NAME)
    with open("products.json") as products_file:
        products_file_data = json.load(products_file)
    products_manager.insert_json_to_collection(products_file_data)
    return products_manager

def main():
    products_manager = create_collection()
    # print("The brands we have are:")
    # print(products_manager.get_brand_names())
    print("get all categories")
    print(products_manager.get_all_categories())
    print("get all color types of shirts")
    print(products_manager.get_all_shirts_colors())
    print("get sums of all items")
    pprint.pprint(list(products_manager.count_all_products()))



if __name__ == '__main__':
    main()