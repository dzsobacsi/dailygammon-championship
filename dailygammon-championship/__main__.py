import os
import sys
import pandas as pd
from matchfile import matchfile
from match_result import match_result
from dotenv import load_dotenv
load_dotenv()

USERID = os.getenv("USERID")
PASSWORD = os.getenv("PASSWORD")
cookies = {"USERID": USERID, "PASSWORD": PASSWORD}
matchIds = []
players_set = set()

if len(sys.argv) < 2:
    sys.exit("Input file name is missing\nUsage example: python dailygammon-championship input.txt")

with open(sys.argv[1]) as file:
    matchIds = file.readlines()
    matchIds = [mid[:7] for mid in matchIds]

matchfiles = [matchfile(mid, cookies) for mid in matchIds]
results = [match_result(f) for f in matchfiles]

for i in results:
    if "players" in i:
        players_set.add(i["players"][0])
        players_set.add(i["players"][1])

players = list(players_set)
players = sorted(players, key=str.lower)

results_df = pd.DataFrame(index=players, columns=players)
for i in range(results_df.shape[0]):
    results_df.iloc[i, i] = "----"

columns = ["finished", "won", "lost", "+", "-", "total"]
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
