# video ref: https://www.youtube.com/watch?v=qWYx5neOh2s
import pymongo
from bson.objectid import ObjectId

cluster = # enter the string in replace_cluster_with_this_string.txt
client = pymongo.MongoClient(cluster)
print(client.list_database_names())
db = client.line_bot
print(db.list_collection_names())

states = db.states
state1 = {"name": "alvin", "onoff": True, "flex": ["a", "b", "c"]}
state2 = {"name": "john", "onoff": False, "flex": [1, 2, 3]}
# result = states.insert_one(state1)
# result = states.replace_one({"_id": ObjectId("61d7363db23cc7cb5c674635")}, state2)
result = states.find_one({"_id": ObjectId("61d7363db23cc7cb5c674635")})

print(result, type(result))
