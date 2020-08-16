#!/usr/bin/python3
import requests
import json
import os
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
    lines = r.text.splitlines()

    players = get_players()

    return {
        "match-id": mid,
        "players": players,
        "winner": players[get_winner()],
        "score": get_points()
    }


USERID = os.getenv("USERID")
PASSWORD = os.getenv("PASSWORD")
matches = []

with open("input.txt") as file:
    data = json.load(file)
    matches = data['matches']

for i in matches:
    result = match_result(i)
    print("Match-ID: {}\nPlayers: {}\nWinner: {}\nScore: {}\n"
        .format(result["match-id"], result["players"], result["winner"], result["score"]))
