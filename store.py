from pymongo import MongoClient

client = MongoClient()
db = client['lol_mm_db']

def get_champion_full():
    # return db['champion_full.v.7.16.1']
    return db['champion_full']

def get_items():
    return db['static_data.items']


def get_match_infos():
    return db['match_infos']