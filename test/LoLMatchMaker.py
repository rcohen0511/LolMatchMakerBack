from pprint import pprint
from riotwatcher import RiotWatcher
import json
import pymysql
import riot
import static_data

conn = pymysql.connect(host='localhost', port=3306, user='Rob', passwd='FcGeyv44', db='leagueDB')
cur = conn.cursor()

watcher = RiotWatcher('RGAPI-6ae1e685-0a84-4e95-adf3-870eff8a5eb9')
region = 'na1'
summoner = 'LordSubie'


# Functions to build static data
def getItemsById():
    items = watcher.static_data.items(region)
    items = json.dumps(items, indent=4)
    print(items)
    return(items)

def getMasteriesById():
    masteries = watcher.static_data.masteries(region)
    pprint(masteries['data'])
    return(masteries['data'])

def getRunesById():
    runes = json.loads(watcher.static_data.runes(region))
    print(runes)
    return(runes)

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

def getPlayerMatchInfo(gameId, summoner):
    recentMatch = watcher.match.by_id(region, gameId)
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
    #======================== Skills and Items =========================#
    match = watcher.match.timeline_by_match(region, gameId)
    skillMap = []
    for i in range(3):
        print(static_data.championFull["data"][champPlayed]['spells'][i])

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





def getItems(gameId,participantId, match):
    # learn here: https://www.python-course.eu/lambda.php
    def filterItems(events, participant_id):
        return filter(lambda e: e.get('type') in ['ITEM_PURCHASED'] and
                                e.get('participantId') == participant_id,
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
                'name': items_map.get(str(e.get('itemId'))).get('name'),
                'type': e.get('type'),
                'description': items_map.get(str(e.get('itemId'))).get('description'),
                'plaintext': items_map.get(str(e.get('itemId'))).get('plaintext'),
            })
        n_events_of_events.append(n_events)
    return(n_events_of_events)
    # return jsonify(
    #     {
    #         "events_of_events": n_events_of_events
    #     })


# Build static data
# masteries = {}
# runes = {}
# masteries = getMasteriesById()
# runes = getRunesById()
# champsByID = getChampionListById()
# items = getItemsById()

getPlayerMatchInfo(2611304278,'Lord Subie')

gameIds = [2611304278, 2612301378]
conn.commit()

print(static_data.championFull)
champPlayed = 'Veigar'
for i in range(3):
    print(static_data.championFull["data"][champPlayed]['spells'][i])