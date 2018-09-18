import json
import requests
from statsmodels.stats.proportion import proportion_confint

def fetch_data(token): # fetch data from splatnet2
    url = "https://app.splatoon2.nintendo.net/api/records"
    cookie = dict(iksm_session=token)
    r = requests.get(url, cookies=cookie)
    return json.loads(r.text)

token = input("Enter SplatNet2 token here: ")
data = fetch_data(token)
weapon_stats = data["records"]["weapon_stats"]

for _,weapon in weapon_stats.items(): # calculate score for all weapons
    wins = weapon["win_count"]
    losses = weapon["lose_count"]
    score_lb, score_hb = proportion_confint(wins, wins+losses, method='beta')
    weapon["score_lb"] = score_lb

sort_weapons = sorted(weapon_stats.values(),
                      key=lambda x: x["score_lb"],
                      reverse=True)

for weapon in sort_weapons:
    print("%s: %f" % (weapon["weapon"]["name"], weapon["score_lb"]))
