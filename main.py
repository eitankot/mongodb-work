from __future__ import annotations
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

def test_max_to_min(products_manager: ProductsManager):
    max_before_changing = products_manager.collection.find_one({"categories": "suits"}, sort=[("price", -1)])
    min_before_changing = products_manager.collection.find_one({"categories": "suits"}, sort=[("price", 1)])
    print(f"max suit before update price = {max_before_changing["price"]}, id = {max_before_changing["_id"]}")
    print(f"min suit before update price = {min_before_changing["price"]}, id = {min_before_changing["_id"]}")
    products_manager.update_max_to_min("suits", "price")
    max_after_changing = products_manager.collection.find_one({"categories": "suits"}, sort=[("price", -1)])
    min_after_changing = products_manager.collection.find_one({"categories": "suits"}, sort=[("price", 1)])
    print(f"max suit after update price = {max_after_changing["price"]}, id = {max_after_changing["_id"]}")
    print(f"min suit after update price = {min_after_changing["price"]}, id = {min_after_changing["_id"]}")

def test_change_all(products_manager: ProductsManager) -> None:
    before = products_manager.collection.find_one()
    before_price = before["price"]
    before_id = before["_id"]
    print(f"BEFORE: item {before_id} in price {before_price}")
    products_manager.change_value_for_all("price", 3)
    after = products_manager.collection.find_one({"_id": before_id})
    after_id = after["_id"]
    after_price = after["price"]
    print(f"AFTER: item {after_id} in price {after_price}")

def test_fix_price(products_manager: ProductsManager):
    products_manager.fix_price("ties", "price", 20)
    print("ties that are not 20 (supposed to be []):")
    print(list(tie for tie in products_manager.collection.find({"categories": "ties", "price": {"$ne": 20}})))


def main():
    products_manager = create_collection()
    products_manager.client.drop_database(DB_NAME)
    products_manager.insert_json_to_collection("products.json")
    test_fix_price(products_manager)
    test_max_to_min(products_manager)
    test_change_all(products_manager)


if __name__ == '__main__':
    main()
