import store

# gets all
for i in store.get_items().find():
    print i


# get by id
store.get_items().find_one({
    'id': 3107
})
