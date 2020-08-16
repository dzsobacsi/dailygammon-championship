#!/usr/bin/python3
import requests
import os
import pprint
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def match_result(mid):
    """
    this function returns a dictionary with the match id, the player names,
    the winner and the match score

    mid: dailygammon match-id as an integer
    """
    def get_winner():
        str = lines[-1]
        if "and the match" not in str:
            print("something is wrong with the winner function argument")
            return None
        spaces_before = 0
        for i in str:
            if i.isspace():
                spaces_before += 1
            else:
                break
        return 1 if spaces_before > 6 else 0

    def get_points():
        i = len(lines) - 1
        while lines[i].split()[0] != players[0]:
            i -= 1
        points = lines[i].split()
        points = [points[2], points[5]]
        points[get_winner()] = '11'
        points = list(map(int, points))
        return points

    def get_players():
        players = lines[3].split()
        return [players[0], players[3]]

    URL = "http://dailygammon.com/bg/export/" + str(mid)
    cookies = {"USERID": USERID, "PASSWORD": PASSWORD}
    r = requests.get(URL, cookies=cookies)

    if r.headers["content-type"] != "text/plain":
        return {
            "match-id": mid,
            "warning": "the match is not finished yet"
        }

    lines = r.text.splitlines()
    players = get_players()

    return {
        "match-id": mid,
        "players": players,
        "winner": get_winner(),
        "score": get_points()
    }


USERID = os.getenv("USERID")
PASSWORD = os.getenv("PASSWORD")
matchIds = []
results = []
players_set = set()

with open("input.txt") as file:
    matchIds = file.readlines()
    matchIds = list(map(int, matchIds))

for i in matchIds:
    results.append(match_result(i))

#pprint.pp(results)
for i in results:
    if "players" in i:
        players_set.add(i["players"][0])
        players_set.add(i["players"][1])

#print("\n")
players = list(players_set)
players = sorted(players, key=str.lower)
columns = ["won", "lost", "+", "-", "total"]
results_df = pd.DataFrame(index=players, columns=players)
summary_df = pd.DataFrame(index=players, columns=columns)
summary_df = summary_df.fillna(0)

for res in results:
    if "players" in res:
        ply = res["players"]
        scr = res["score"]
        wnr = res["winner"]
        results_df.loc[ply[0], ply[1]] = str(scr[0]) + ":" + str(scr[1])
        summary_df.loc[ply[wnr], "won"] += 1
        summary_df.loc[ply[1-wnr], "lost"] += 1
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
