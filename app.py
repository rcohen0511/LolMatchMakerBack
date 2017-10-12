import league_api
import json
from collections import OrderedDict
from flask import Flask, jsonify
from riotwatcher import RiotWatcher
import riot
import static_data
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/matches/<champPlayed>/<champPlayedOpp>")
def matches(champPlayed, champPlayedOpp):
    print champPlayed
    print champPlayedOpp

    data = league_api.get_matches(champPlayed, champPlayedOpp)
    print(data)
    data = data[0][1:]
    # return jsonify({"data": {"items": json.loads(data[7])}})
    return jsonify({
        "champPlayed": data[0],
        "champId": data[1],
        "summonerName": data[2],
        "accountId": data[3],
        "gameId": data[4],
        "lane": data[5],
        "runes": json.loads(data[6]),
        "masteries": json.loads(data[7]),
        "items": json.loads(data[8]),
        "skills": json.loads(data[9]),
        "team": data[10],
        "opponentSummoner": data[11],
        "opponentAccountId": data[12],
        "opponentChampion": data[13]
    })
    # return jsonify({ "data": {
    #     "items": json.loads(data)
    # }})


@app.route("/api/items")
def get_items():
    def filter_items(events, participant_id):
        # return filter(lambda e: e.get('type') in ['ITEM_PURCHASED', 'ITEM_UNDO']  and e.get('participantId') == participant_id, events)
        return filter(lambda e: e.get('type') in ['ITEM_PURCHASED'] and e.get('participantId') == participant_id,
                      events)

    participant_id = 1
    game_id = 2611304278
    # TODO move out later
    # watcher = RiotWatcher('RGAPI-d31bbdbe-2725-4e12-9037-218e24352f71')
    # match = watcher.match.timeline_by_match(region, game_id)
    match = riot.get_match(game_id)
    items_map = static_data.items
    print items_map

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
    return jsonify(
        {
            "events_of_events": n_events_of_events
        })


if __name__ == "__main__":
    static_data.load()
    app.run(debug=True)