import riot
import json
import store

# items = None
items = dict([(item.get('id'), item)for item in store.get_items().find()])
masteries = None
runes = None
champions = None
championFull = None

def load():
    global items
    global masteries
    global champions
    global championFull

    items = dict([(item.get('id'), item)for item in store.get_items().find()])