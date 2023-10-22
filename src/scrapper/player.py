
from bs4 import BeautifulSoup
import json
import requests

STAT_TYPES = ["BATTING", "BOWLING", "FIELDING", "ALLROUND"]
RECORD_CLASS_ID = {"TEST": 1, "ODI": 2, "TEST": 3}
STATS_URL = "https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats/summary?playerId={player_id}&recordClassId={record_class}&type={stat_type}"
DNB = "Didn't Bat"


def get_filename_from_player_name(player_name: str):
    player_name = player_name.lower().replace(" ", "_")
    return player_name


def get_odi_urls(player_id):
    urls = dict()
    for stat_type in STAT_TYPES:
        url = STATS_URL.format(
            player_id=player_id, record_class=RECORD_CLASS_ID["ODI"], stat_type=stat_type
        )
        urls[stat_type] = url
    return urls


def get_summary_statistics(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return {}
    stats = r.json()
    return stats


def get_odi_match_records(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return {}

    matches = []
    soup = BeautifulSoup(r.text)
    tb = soup.find("caption", string="Match by match list").parent
    tbody = tb.findChild("tbody")
    trows = tbody.findChildren("tr")
    for trow in trows:
        tds = trow.findChildren("td")
        runs_no = tds[0].text
        runs = runs_no.replace("*", "")
        no = str(runs_no).find("*") != -1
        wickets = tds[1].text
        runs_conceded = tds[2].text
        catches_taken = tds[3].text
        stumpings_made = tds[4].text
        opposition = tds[6].text
        ground = tds[7].text
        date = tds[8].text
        
        match = {
            "runs": runs, "not_out": no, "wickets": wickets, "runs_conceded": runs_conceded, "catches_taken": catches_taken, "stumpings_made": stumpings_made, "opposition": opposition, "ground": ground, "date": date,
        }
        matches.append(match)
    return matches



def load_player_urls(path: str):
    with open(path, "r") as fp:
        player_urls = json.load(fp)
    return player_urls


if __name__ == "__main__":
    save_dir = "./data/players"
    players_urls_path = "./data/players.json"
    players_urls = load_player_urls(players_urls_path)

    for player_name in players_urls:
        print(f"Scrapping information on: {player_name}")
        player_id = players_urls[player_name]["player_id"]
        profile_url = players_urls[player_name]["profile"]
        statistics_url = players_urls[player_name]["statistics"]
        odi_matches_url = players_urls[player_name]["odi_matches"]

        odi_matches = get_odi_match_records(odi_matches_url)

        urls = get_odi_urls(player_id)
        stats = dict()
        stats["player_id"] = player_id
        stats["player"] = player_name
        stats["odi_matches"] = odi_matches

        for stat_type, url in urls.items():
            stat = get_summary_statistics(url)
            stats[stat_type] = stat

        with open(save_dir + f"/{get_filename_from_player_name(player_name)}.json", "w") as fp:
            json.dump(stats, fp, indent=4)
        