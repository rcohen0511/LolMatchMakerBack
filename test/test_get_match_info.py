from pprint import pprint
from riotwatcher import RiotWatcher
import json
import riot
import config
import store
import static_data

watcher = RiotWatcher(config.RIOT_KEY)
region = 'na1'


def getItems(gameId,participantId, match):
    def filterItems(events, participant_id):
        return filter(lambda e: e.get('type') in ['ITEM_PURCHASED'] and e.get('participantId') == participant_id,
                      events)

    items_map = static_data.items
    events = [filterItems(f.get('events'), participantId) for f in match['frames']]
    events_of_events = [x for x in events if x != []]

    n_events_of_events = []
    for events in events_of_events:
        n_events = []
        for e in events:
            n_events.append({
                'itemId': e.get('itemId'),
                'name': items_map.get(e.get('itemId')).get('name'),
                'type': e.get('type'),
                'description': items_map.get(e.get('itemId')).get('description'),
                'plaintext': items_map.get(e.get('itemId')).get('plaintext'),
            })
        n_events_of_events.append(n_events)
    return(n_events_of_events)


def getPlayerMatchInfo(gameId, summoner):
    '''
    gameId = 2611304278
    summoner = 'Lord Subie'
    :param gameId:
    :param summoner:
    :return:
    '''
    recentMatch = watcher.match.by_id(region, gameId)
    # ================ Get Player Info =====================================#
    i = 0
    while i <= 9:
        if recentMatch['participantIdentities'][i]['player']['summonerName'] == summoner:
            participantId = recentMatch['participantIdentities'][i]['participantId']
            accountId = recentMatch['participantIdentities'][i]['player']['accountId']
            break
        i = i + 1

    champion_key = str((recentMatch)['participants'][participantId - 1]['championId'])
    champPlayed = store.get_champion_full().find_one({
        'key': champion_key
    })

    # champPlayed = str(champsByID[(recentMatch)['participants'][participantId - 1]['championId']])

    # champID = str(recentMatch['participants'][participantId - 1]['championId'])
    champID = champion_key
    summonerName = summoner
    accountId = str(accountId)
    gameId = str(gameId)
    team = str(recentMatch['participants'][participantId - 1]['teamId'])
    lane = str(recentMatch['participants'][participantId - 1]['timeline']['lane'])
    runes = recentMatch['participants'][participantId - 1]['runes']
    # ==================== Masteries ===================================#
    # cleanMasteries = {}
    # masteries = recentMatch['participants'][participantId - 1]['masteries']
    # for mastery in masteries:
    #     cleanMasteries[mastery['masteryId']] = {'masteryId': mastery['masteryId'], 'rank': mastery['rank']}
    # masteries = json.dumps(cleanMasteries)
    #======================== Skills and Items =========================#
    match = watcher.match.timeline_by_match(region, gameId)
    # skillMap = []
    # for i in range(3):
    #     print(static_data.championFull["data"][champPlayed]['spells'][i])

    itemList = []
    skillOrder = {}
    skillNum = 0
    for frame in match['frames']:
        # print("Frame: "+str(frame['timestamp']))
        for obj in frame['events']:
            try:
                if obj['type'] == 'SKILL_LEVEL_UP':
                    if obj['participantId'] == participantId:
                        skillOrder[skillNum] = obj['skillSlot']
                        skillNum += 1
                # AT SOME POINT SHOULD PUT SOMETHING FOR SOLD ITEMS
                # elif obj['type'] == 'ITEM_DESTROYED':
            except:
                pass

    itemList = getItems(gameId, participantId, match)
    #==================== Opponent info ================================#
    i = 0
    while i <= 9:
        if str(recentMatch['participants'][i]['timeline']['lane']) == lane and str(recentMatch['participants'][i]['teamId']) != team:
            opponentParticipantId = recentMatch['participantIdentities'][i]['participantId']
            opponentAccountId = str(recentMatch['participantIdentities'][i]['player']['accountId'])
            opponentSummoner = str(recentMatch['participantIdentities'][i]['player']['summonerName'])
            break
        i = i + 1

    champion_key = str((recentMatch)['participants'][opponentParticipantId - 1]['championId'])
    opponentChampion = store.get_champion_full().find_one({
        'key': champion_key
    })

    match_info = {
        "gameId": gameId,
        "summonerName": summonerName,
        "team": team,
        "accountId": accountId,
        "champId": champID,
        "champPlayed": champPlayed.get('name'),
        "opponentAccountId": opponentAccountId,
        "opponentChampion": opponentChampion.get('name'),
        "opponentSummoner": opponentSummoner,
        "items": itemList,
        "skills": [],
        "runes": runes,
    }

    # return (dataToSQL)




pro_players = ['Dyrus', ]






get_recent_game_ids('Lord Subie')