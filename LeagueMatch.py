from pprint import pprint
from riotwatcher import RiotWatcher
import json
import pymongo
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='Rob', passwd='FcGeyv44', db='leagueDB')
cur = conn.cursor()

# client = pymongo.MongoClient()
# collection = client.test.restaurants

watcher = RiotWatcher('RGAPI-d31bbdbe-2725-4e12-9037-218e24352f71')
region = 'na1'
summoner = 'LordSubie'

def getPlayerAccountId(summonerName):
    player = watcher.summoner.by_name(region, summonerName)
    accountId = player.get('accountId')
    print("Found AccountId for "+summonerName+" it is: "+str(accountId))
    return(accountId)

def getRecentMatchHistory(summonerName):
    gameIds = []
    accountId = getPlayerAccountId(summonerName)
    matches = watcher.match.matchlist_by_account_recent(region, accountId)
    for match in matches['matches']:
        # match item contains, lane played, champion played, role and others
        gameIds += [match['gameId'],]
    print("gameId's found for "+summonerName+" are: ")
    print(gameIds)
    return(gameIds)

def getMostRecentGameId(summonerName):
    gameIds = getRecentMatchHistory(summonerName)
    print("Most Recent Game Id for: "+summonerName+" is "+str(gameIds[0]))
    return(gameIds[0])

def getMatchInfo(gameId):
    # Lists players in a game that are assigned participantIds 1-10
    match = watcher.match.by_id(region, gameId)
    return(match)

def getParticipants(gameId):
    match = watcher.match.by_id(region, gameId)
    return (match)

def getParticipantInfo(gameId):
    participants = getParticipants(gameId)
    #different index maps to dif participant 0=1, 1=2...through 9=10
    matchInfo = participants[0]
    pprint(matchInfo)
    return(matchInfo)

def getParticipantIdInGame(summonerName, gameId):
    identities = getMatchInfo(gameId)
    for identity in identities:
        print(identity)

def getChampionListById():
    championsById = {}
    champions = {}
    champions = watcher.static_data.champions(region)
    for champion in champions['data']:
        champId = champions['data'][champion]['id']
        champKey = champions['data'][champion]['key'].encode("utf-8")
        championsById[champId] = champKey
    print("Got list of Champions by Id: ")
    pprint(championsById)
    return championsById

def getMasteriesById():
    masteries = watcher.static_data.masteries(region)
    pprint(masteries['data'])
    return(masteries['data'])

def getRunesById():
    runes = json.loads(watcher.static_data.runes(region))
    print(runes)
    return(runes)

def getPlayerMatchInfo(gameId, summoner):
    recentMatch = getMatchInfo(gameId)
    # ================ Get Player Info =====================================#
    i = 0
    while i <= 9:
        if recentMatch['participantIdentities'][i]['player']['summonerName'] == summoner:
            participantId = recentMatch['participantIdentities'][i]['participantId']
            accountId = recentMatch['participantIdentities'][i]['player']['accountId']
            break
        i = i + 1
    champPlayed = str(champsByID[(recentMatch)['participants'][participantId - 1]['championId']])
    champID = str(recentMatch['participants'][participantId - 1]['championId'])
    summonerName = summoner
    accountId = str(accountId)
    gameId = str(gameId)
    team = str(recentMatch['participants'][participantId - 1]['teamId'])
    lane = str(recentMatch['participants'][participantId - 1]['timeline']['lane'])
    runes = json.dumps(recentMatch['participants'][participantId - 1]['runes'])
    # ==================== Masteries ===================================#
    cleanMasteries = {}
    masteries = recentMatch['participants'][participantId - 1]['masteries']
    for mastery in masteries:
        cleanMasteries[mastery['masteryId']] = {'masteryId': mastery['masteryId'], 'rank': mastery['rank']}
    masteries = json.dumps(cleanMasteries)
    #======================== Items ====================================#
    # itemList = {}
    # stats = recentMatch['participants'][participantId - 1]['stats']
    # for stat in stats:
    #     if stat.startswith('item'):
    #         itemList[stat] = recentMatch['participants'][participantId - 1]['stats'][stat]
    # items = json.dumps(itemList)
    match = watcher.match.timeline_by_match(region, gameId)
    itemList = {}
    skillOrder = {}
    itemNum = 0
    skillNum = 0
    for frame in match['frames']:
        # print("Frame: "+str(frame['timestamp']))
        for obj in frame['events']:
            try:
                if obj['type'] == 'ITEM_PURCHASED':
                    if obj['participantId'] == participantId:
                        itemList[itemNum] = obj['itemId']
                        itemNum += 1
                elif obj['type'] == 'SKILL_LEVEL_UP':
                    if obj['participantId'] == participantId:
                        skillOrder[skillNum] = obj['skillSlot']
                        skillNum += 1
                # AT SOME POINT SHOULD PUT SOMETHING FOR SOLD ITEMS
                # elif obj['type'] == 'ITEM_DESTROYED':
            except:
                pass
    items = json.dumps(itemList, sort_keys=True)
    skills = json.dumps(skillOrder, sort_keys=True)
    #==================== Opponent info ================================#
    i = 0
    while i <= 9:
        if str(recentMatch['participants'][i]['timeline']['lane']) == lane and str(recentMatch['participants'][i]['teamId']) != team:
            opponentParticipantId = recentMatch['participantIdentities'][i]['participantId']
            opponentAccountId = str(recentMatch['participantIdentities'][i]['player']['accountId'])
            opponentSummoner = str(recentMatch['participantIdentities'][i]['player']['summonerName'])
            break
        i = i + 1
    opponentChampion = champsByID[(recentMatch)['participants'][opponentParticipantId - 1]['championId']]
    #======================== SQL =======================================#
    dataToSQL = (champPlayed,champID,summonerName,accountId,gameId,lane,runes,masteries,items,skills, team,opponentSummoner,opponentAccountId,opponentChampion)
    cur.execute("insert into matches values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s,%s, %s)", dataToSQL)
    conn.commit()
    return (dataToSQL)

def getItemsById():
    items = watcher.static_data.items(region)
    items = json.dumps(items, indent=4)
    print(items)
    return(items)


# Build static data
masteries = {}
runes = {}
masteries = getMasteriesById()
runes = getRunesById()
champsByID = getChampionListById()
items = getItemsById()

print(runes[2])

pprint(watcher.static_data.runes(region))


match = watcher.match.timeline_by_match(region, 2611304278)
test = json.dumps(match, indent=4)
print(test['frames']['events'])
pprint(len(match['frames']))
pprint(match['frames'])
pprint(match['frames'][1]['events'])
watcher.match.timeline_by_match(2611304278)


def fullMatchInfo():

    winningTeam = ""
    gameLength = ""
    blueBans = ""
    redBans = ""
    dataToSQL = ()
    return dataToSQL

print(getMostRecentGameId('Lord Subie'))
recentMatch = getMatchInfo(2612301378)
pprint(recentMatch['participantIdentities'])

getPlayerMatchInfo(2612301378,'Lord Subie')


conn.commit()




###
#


def get_items():
    def filter_items(events, participant_id):
        # return filter(lambda e: e.get('type') in ['ITEM_PURCHASED', 'ITEM_UNDO']  and e.get('participantId') == participant_id, events)
        return filter(lambda e: e.get('type') in ['ITEM_PURCHASED'] and e.get('participantId') == participant_id,
                      events)

    def get_items_map():
        return watcher.static_data.items(region).get('data')

    participant_id = 1
    game_id = 2611304278
    region = 'na1'
    match = watcher.match.timeline_by_match(region, game_id)
    items_map = get_items_map()

    events = [filter_items(f.get('events'), participant_id) for f in match['frames']]
    events_of_events = [x for x in events if x != []]

    n_events_of_events = []
    for events in events_of_events:
        n_events = []
        for e in events:
            n_events.append({
                'item_id': e.get('itemId'),
                'name': items_map.get(str(e.get('itemId'))).get('name'),
                'type': e.get('type'),
            })
        n_events_of_events.append(n_events)
    return n_events_of_events

n_events_of_events = get_items()

# pprint(items.get('3020'))

pprint(n_events_of_events)

json.dumps(n_events_of_events)

# norm_data = [[{
#     'item_id': e.get('itemId'),
#     'name': items.get(e.get('itemId'))
#     'type': e.get('type')
# } for e in ee] for ee in events]

pprint(norm_data)
