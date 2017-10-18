import json
import riot
import store

def import_items():
    items = riot.get_items()
    for v in items.values():
        store.get_items().insert_one(v)


def import_champion_full():
    with open('json/championFull.json') as data_file:
        data = json.load(data_file)

    for v in data.get('data').values():
        store.get_champion_full().insert_one(v)


def import_all():
    import_items()
    import_champion_full()