import json
from pymongo import MongoClient
from CourseShop import ProductsManager

DB_NAME = "Products"
COLLECTION_NAME = "Inventory"


def main():
    products_manager = ProductsManager()
    with open("products.json") as products_file:
        products_file_data = json.load(products_file)
    products_manager.insert_json_to_collection(DB_NAME, COLLECTION_NAME, products_file_data)
    print("The brands we have are:")
    print(products_manager.get_brand_names(DB_NAME, COLLECTION_NAME))


if __name__ == '__main__':
    main()