import pymongo
from bson.objectid import ObjectId
import json

# State of the devices
# - Fan
fan_id = "a00abf394b1c"
fan_on = None  # True, False
fan_speed = -1  # int
fan_turn = None  # True, False
# - A/C
ac_id = "a00abf1dd7e7"
ac_on = None  # True, False
ac_set_temp = -1  # int
ac_ambient_temp = -1  # int 
# - A/F
af_id = "a00abf1ddb09"
af_on = None  # True, False
af_pm25 = -1.  # float
# - vacuum - FIXME: no vacuum yet, can't update state, temporally init as off
vacuum_id = "no_id_yet"
vacuum_on = False  # remember to update state manually

#FIXME: what's the init tab?
current_tab = "scenario"  # {scenario, living_room, master_bedroom, elder_bedroom}

# State of the scenario setting
scenarios_on_off = {
    "go_home_on": ["ac_box", "add_box"],
    "go_home_off": ["af_box", "vacuum_box", "add_box"],
    "all_go_home_on": ["add_box"],
    "all_go_home_off": ["add_box"],
    "go_out_on": ["add_box"],
    "go_out_off": ["add_box"],
    "night_on": ["add_box"],
    "night_off": ["add_box"],
    "morning_on": ["add_box"],
    "morning_off": ["add_box"],
    "noon_on": ["add_box"],
    "noon_off": ["add_box"]
}

# re-new a document on MongoDB
cluster = # enter the string in replace_cluster_with_this_string.txt
client = pymongo.MongoClient(cluster)
print(client.list_database_names())
db = client.line_bot
print(db.list_collection_names())
states = db.states
state0 = {
    "fan_on": fan_on,
    "fan_speed": fan_speed,
    "fan_turn": fan_turn,
    "ac_on": ac_on,
    "ac_set_temp": ac_set_temp,
    "ac_ambient_temp": ac_ambient_temp,
    "af_on": af_on,
    "af_pm25": af_pm25,
    "vacuum_on": vacuum_on,
    "current_tab": current_tab,
    "scenarios_on_off": scenarios_on_off
}
result = states.replace_one({"_id": ObjectId("61d7363db23cc7cb5c674635")}, state0)
result = states.find_one({"_id": ObjectId("61d7363db23cc7cb5c674635")})
print(f"MongoDB: {result=}")
result["_id"] = str(result["_id"])
with open("./doc.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(fan_on)
for key, value in result.items():
    if key != "_id":
        globals()[key] = value
print(fan_on)