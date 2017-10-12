from riotwatcher import RiotWatcher

watcher = RiotWatcher('RGAPI-d31bbdbe-2725-4e12-9037-218e24352f71')
region = 'na1'

def get_match(game_id):
    return watcher.match.timeline_by_match(region, game_id)

def get_items():
    watcher.static_data.items(region).get('data')
