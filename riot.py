from riotwatcher import RiotWatcher
from pprint import pprint
import config

watcher = RiotWatcher(config.RIOT_KEY)
region = 'na1'

def getMatch(game_id):
    return watcher.match.timeline_by_match(region, game_id)

def get_items():
    return watcher.static_data.items(region).get('data')


def get_champions():
    champions = watcher.static_data.champions(region).get('data')
    watcher.champion.by_id()
    pprint(champions)

    return champions

