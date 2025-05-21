from typing import Optional, List
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId

from .models import UserInDB, MessageInDB, PyObjectId


async def get_user_id(user_collection: Collection, username: str) -> Optional[PyObjectId]:
    rv = await user_collection.find_one(
        {'username': username},
        {'_id': 1}
    )
    return PyObjectId(rv['_id']) if rv else None
