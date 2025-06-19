from __future__ import annotations
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
    print(list(i for i in products_manager.count_sizes()))


if __name__ == '__main__':
    main()
