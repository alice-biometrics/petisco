from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def mongodb_is_running_locally(
    host="localhost", port=27017, username="root", password="password123"
) -> bool:
    mongo_client = MongoClient(
        f"mongodb://{host}:{port}/",
        username=username,
        password=password,
        serverSelectionTimeoutMS=1000,
    )
    try:
        # The ismaster command is cheap and does not require auth.
        mongo_client.admin.command("ismaster")
    except ConnectionFailure:
        return False
    return True
