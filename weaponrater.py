import json
import operator
import requests

def fetch_data(token): # fetch data from splatnet2
    url = "https://app.splatoon2.nintendo.net/api/records"
    cookie = dict(iksm_session=token)
    r = requests.get(url, cookies=cookie)
    return json.loads(r.text)

def wilson_score_lb(w, l):
    n = w + l
    if n > 0:
        z = 1.96 # magic number representing 95%
        return (w+z**2/2)/(n+z**2)-(z/(n+z**2))*(w*l/n+z**2/4)**(1/2)
    else:
        return 0

token = input("Enter SplatNet2 token here: ")
data = fetch_data(token)
weapon_stats = data["records"]["weapon_stats"]

for _,weapon in weapon_stats.items(): # calculate wilson score for all weapons
    wins = weapon["win_count"]
    losses = weapon["lose_count"]
    score = wilson_score_lb(wins, losses)
    weapon["wilson_score_lb"] = score

sort_weapons = sorted(weapon_stats.values(),
                      key=lambda x: x["wilson_score_lb"],
                      reverse=True)

for weapon in sort_weapons:
    print("%s: %f" % (weapon["weapon"]["name"], weapon["wilson_score_lb"]))
