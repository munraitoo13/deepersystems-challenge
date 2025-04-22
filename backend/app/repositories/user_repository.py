from pymongo.collection import Collection
from bson import ObjectId


class UserRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_all(self):
        return list(self.collection.find())

    def find_by_id(self, user_id: ObjectId):
        return self.collection.find_one({"_id": user_id})

    def create(self, user_dict: dict) -> ObjectId:
        return self.collection.insert_one(user_dict).inserted_id

    def update(self, user_id: ObjectId, update_dict: dict) -> bool:
        return (
            self.collection.update_one(
                {"_id": user_id}, {"$set": update_dict}
            ).modified_count
            > 0
        )

    def delete(self, user_id: ObjectId) -> bool:
        return self.collection.delete_one({"_id": user_id}).deleted_count > 0
