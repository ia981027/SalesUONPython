from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:27017/"

client = MongoClient(uri, server_api=ServerApi("1"))

db = client["UON"]


def insert_one(doc: dict, collection_name: str = "SalesPython") -> str | int:
    return db[collection_name].insert_one(doc).inserted_id


def delete_one(doc: dict, collection_name: str = "SalesPython"):
    return db[collection_name].delete_one(doc)


def delete_many(doc: dict, collection_name: str = "SalesPython"):
    return db[collection_name].delete_many(doc)


def insert_many(
    docs: list[dict], collection_name: str = "SalesPython"
) -> list[str | int]:
    try:
        return db[collection_name].insert_many(docs).inserted_ids
    except TypeError:
        print(f"Failed to insert {docs=} into {collection_name=}")
        return []


def find(item: dict = {}, collection_name: str = "SalesPython") -> list:
    if item:
        return [result for result in db[collection_name].find(item)]
    else:
        return [result for result in db[collection_name].find()]
