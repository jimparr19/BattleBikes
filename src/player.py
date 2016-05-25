from pymongo import MongoClient
from bson.objectid import ObjectId
import time
"""
|------|  |------|
| cl 1 |  | cl 2 |
|------|  |------|

|----------------|
| Flask Server   |
|----------------|

|----------------|
| Mongo Database |
|----------------|

|----------------|
| Tcp Server     |
|----------------|

|------|  |------|
| pi 1 |  | pi 2 |
|------|  |------|
Assuming max of two players.
Player one connects
Player one awaits challenger...
Player one awaits challenger...
Player two connects
Player one gets challenger id (player two)
Player two gets challenger id (player one)
<synchronise times>
Battle Begins!
    pi_1 pushes data
    pi_2 pushes data
    cl_1 pulls data, receives player 1 and 2 data
    cl_2 pulls data, receives plater 1 and 2 data
"""


class Player:
    def __init__(self, name):
        self.collection_name = name
        self.client = None
        self.db = None
        self.collection = None
        self._id = None

    def start(self):
        self.client = MongoClient()
        self.db = self.client['BattleBikes']
        self.collection = self.db[self.collection_name]
        #self.collection.delete_many({})

        #initial_entry = {"speed": []}


    def update_speed(self, latest_speeds):
        speed = self.collection.find_one({})['speed']
        # entry['speed'] += latest_speeds
        speed += latest_speeds
        #self.collection.update({"_id": self._id}, {"$set": {"speed": speed}}, upsert=False)

        self.collection.update({}, {"$set": {"speed": speed}}, upsert=False)


    def get_speed(self):
        return self.collection.find_one({})['speed']


def start():
    player_1 = Player("Player1")
    player_2 = Player("Player2")


    player_1.start()
    player_2.start()


    player_1.collection.delete_many({})
    player_2.collection.delete_many({})

    player_1.collection.insert_one({"speed": []}).inserted_id
    player_2.collection.insert_one({"speed": []}).inserted_id

    for i in range(0, 5):
        player_1.update_speed([101, 102, 103])
        player_2.update_speed([201, 202, 203])
        time.sleep(1)
        print(player_1.get_speed())

    #for doc in player_1.collection:
    print(player_1.collection)

    # print(player_1.get_speed())
    # print(player_2.get_speed())

# def main():
#     client = MongoClient()
#     db = client['BattleBikes']
#     cl = db['Player1']
#     cl.delete_many({})
#
#     info = {"speed": [100]}
#
#     _id = cl.insert_one(info).inserted_id
#     print("ID: %s" % _id)
#
#     _cl_names = db.collection_names(include_system_collections=False)
#     print("Names: %s" % _cl_names)
#
#     entry = cl.find_one({"player": 1})
#     print("Entry: %s" % entry)
#
#     for doc in cl.find({}):
#         print(doc)
#
#     for i in range(0, 3):
#         entry['speed'] += [101, 102, 103]
#         #print("Entry: %s" % entry)
#         cl.update({"_id": _id}, {"$set": {"speed": entry['speed']}}, upsert=False)
#
#         entry = cl.find_one({"player": 1})
#         print("Entry: %s" % entry)
#
#         #for doc in cl.find({}):
#         #    print(doc)
#
if __name__ == "__main__":
    start()
