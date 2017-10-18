import json
from riotwatcher import RiotWatcher
from pprint import pprint
import store

watcher = RiotWatcher('RGAPI-c7783c8a-3463-4639-8ba5-a59af13af4db')
region = 'na1'


###
champions = watcher.static_data.champions(region).get('data')
watcher.champion.by_id(region,62)
watcher.champion.all

# spells = watcher.static_data.summoner_spells(region)
# pprint(spells)
# all = watcher.champion.all(region)
# pprint(all)



# pprint(items)
# pprint(champions)


##
# champion full
#  import champion full to mongo db


# def upload():


# pull from mongo db
champion_full = store.get_champion_full().find_one({
    'id': 'MonkeyKing'
})


###
# matches

match = watcher.match.by_id(region, 2612301378)
pprint(match)


