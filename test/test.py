import json
# from leagueoflegends import LeagueOfLegends, RiotError
#
# lol = LeagueOfLegends('RGAPI-6d75f533-0ee4-481b-bbfb-ea58e1da3a18')
#
# # id = lol.get_summoner_by_name('Dyrus')
# id = lol.get_summoner_by_name('RiotSchmick')
# id = lol.get_summoner_by_name('infamousrob')
# lol.get_games(id)
from pprint import pprint

from riotwatcher import RiotWatcher

watcher = RiotWatcher('RGAPI-6d75f533-0ee4-481b-bbfb-ea58e1da3a18')
my_region = 'na1'

# me = watcher.summoner.by_name(my_region, 'lordsubie')
me = watcher.summoner.by_name(my_region, 'RiotSchmick')
print(me)

my_mastery_pages = watcher.masteries.by_summoner(my_region, me['id'])
pprint(my_mastery_pages)

# lets see if i got diamond yet (i probably didnt)
my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
pprint(my_ranked_stats)

### match info

matches = watcher.match.matchlist_by_account_recent(my_region, me['accountId'])
pprint(matches)
# print me['id']

game_id = '2565973154'
m = watcher.match.by_id(my_region, game_id)

pprint(m.keys())
pprint(m)


participant_details = [
    {
        "summoner_name": p.get('player').get('summonerName'),
        "profile_icon": p.get('player').get('profileIcon'),

    }
    for p in m.get('participantIdentities')]



for p in m:
    print("=============================")
    print(p)
    pprint(m.get(p))

def create_match_info(m):
    match_info = {
        "match_id": m.get('gameId'),
        "game_mode": m.get('gameMode'),
        "participant_details": participant_details
    }
    return match_info

match_info = create_match_info(m)

pprint(match_info)

print json.dumps(match_info, indent=4)


def getMastery(championId):
    participants = [
        {
            "championId": p.get('championId'),
            "masteries": p.get('masteries'),
        }]

        # for p in m.get('participants')]

    pprint(participants)