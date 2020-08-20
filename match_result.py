import requests
import os
import re
import sys
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def match_result(mid):
    """
    this function returns a dictionary with the match id, the player names,
    the winner and the match score

    mid: dailygammon match-id as a string
    """
    def get_winner():
        str = lines[-1]
        if "and the match" not in str:
            print("something is wrong with the winner function argument")
            return None
        position = str.find("Wins")
        return 1 if position > 6 else 0

    def get_points():
        i = len(lines) - 1
        while lines[i].split(":")[0].strip() != players[0]:
            i -= 1
        points = lines[i]
        points = re.findall(": \d+", points)
        points = [p[2:] for p in points]
        points[get_winner()] = '11'
        points = list(map(int, points))
        return points

    def get_players():
        players = lines[3]
        players = re.split(" : \d+", players)
        players = [p.strip() for p in players]
        return players[:2]

    URL = "http://dailygammon.com/bg/export/" + mid
    r = requests.get(URL, cookies=cookies)

    if r.headers["content-type"] != "text/plain":
        return {
            "match-id": mid,
            "warning": "the match is not finished yet"
        }

    lines = r.text.splitlines()
    players = get_players()

    #Test output
    #print(mid)
    #print(players)
    #print(get_winner())
    #print(get_points())

    return {
        "match-id": mid,
        "players": players,
        "winner": get_winner(),
        "score": get_points()
    }

#
#    MAIN
#

USERID = os.getenv("USERID")
PASSWORD = os.getenv("PASSWORD")
cookies = {"USERID": USERID, "PASSWORD": PASSWORD}
matchIds = []
players_set = set()

if len(sys.argv) < 2:
    sys.exit("Input file name is missing\nUsage example: python match_result.py input.txt")

with open(sys.argv[1]) as file:
    matchIds = file.readlines()
    matchIds = [mid[:7] for mid in matchIds]

results = [match_result(mid) for mid in matchIds]

for i in results:
    if "players" in i:
        players_set.add(i["players"][0])
        players_set.add(i["players"][1])

players = list(players_set)
players = sorted(players, key=str.lower)
columns = ["finished", "won", "lost", "+", "-", "total"]

results_df = pd.DataFrame(index=players, columns=players)
for i in range(results_df.shape[0]):
    results_df.iloc[i, i] = "----"

summary_df = pd.DataFrame(index=players, columns=columns)
summary_df = summary_df.fillna(0)

for res in results:
    if "players" in res:
        ply = res["players"]
        scr = res["score"]
        wnr = res["winner"]
        results_df.loc[ply[0], ply[1]] = str(scr[0]) + ":" + str(scr[1])
        summary_df.loc[ply[wnr], "won"] += 1
        summary_df.loc[ply[wnr], "finished"] += 1
        summary_df.loc[ply[1-wnr], "lost"] += 1
        summary_df.loc[ply[1-wnr], "finished"] += 1
        summary_df.loc[ply[0], "+"] += scr[0]
        summary_df.loc[ply[0], "-"] -= scr[1]
        summary_df.loc[ply[0], "total"] += scr[0] - scr[1]
        summary_df.loc[ply[1], "+"] += scr[1]
        summary_df.loc[ply[1], "-"] -= scr[0]
        summary_df.loc[ply[1], "total"] += scr[1] - scr[0]

summary_df = summary_df.sort_values(by=["won", "total"], ascending=False)

print("\n")
print(results_df)
print("\n")
print(summary_df)

writer = pd.ExcelWriter(sys.argv[1].split(".")[0] + ".xlsx")
results_df.to_excel(writer, "results")
summary_df.to_excel(writer, "summary")
writer.save()
