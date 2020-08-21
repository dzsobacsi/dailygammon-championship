import re

def match_result(matchfile):
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

    if matchfile["res"].headers["content-type"] != "text/plain":
        return {
            "match-id": matchfile["mid"],
            "warning": "the match is not finished yet"
        }

    lines = matchfile["res"].text.splitlines()
    players = get_players()

    #Test out
    #print(matchfile["mid"])
    #print(players)
    #print(get_winner())
    #print(get_points())
    #print("\n")

    return {
        "match-id": matchfile["mid"],
        "players": players,
        "winner": get_winner(),
        "score": get_points()
    }
