import pymysql


def get_matches(champPlayed, champPlayedOpp):
    conn = pymysql.connect(host='localhost', port=3306, user='Rob', passwd='FcGeyv44', db='leagueDB')
    cur = conn.cursor()
    champPlayed = "%" + champPlayed + "%"
    champPlayedOpp = "%" + champPlayedOpp + "%"
    cur.execute("select * from matches where champPlayed like %s and opponentChampion like %s", (champPlayed, champPlayedOpp))
    rows = []
    for row in cur:
        rows.append(row)
    conn.close()
    return rows
