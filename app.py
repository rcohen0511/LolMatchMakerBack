import league_api
import json
from collections import OrderedDict
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/matches/<champPlayed>/<champPlayedOpp>")
def matches(champPlayed, champPlayedOpp):
    print champPlayed
    print champPlayedOpp

    data = league_api.get_matches(champPlayed, champPlayedOpp)
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
        "team": data[9],
        "opponentSummoner": data[10],
        "opponentAccountId": data[11],
        "opponentChampion": data[12]
    })
    # return jsonify({ "data": {
    #     "items": json.loads(data)
    # }})

if __name__ == "__main__":
    app.run(debug=True)