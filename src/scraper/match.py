from bs4 import BeautifulSoup
import json
import requests

MATCH_URL = "https://www.espncricinfo.com/matches/engine/match/{match_id}.json"


def get_filename_from_player_name(player_name: str):
    player_name = player_name.lower().replace(" ", "_")
    return player_name


def get_odi_match_details(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return {}
    stats = r.json()
    return stats


def load_player_urls(path: str):
    with open(path, "r") as fp:
        player_urls = json.load(fp)
    return player_urls


def load_player_details(path: str):
    with open(path, "r") as fp:
        player_details = json.load(fp)
    return player_details


if __name__ == "__main__":
    save_dir = "./data/odi_matches"
    player_data_dir = "./data/players"
    players_urls_path = "./data/players.json"
    players_urls = load_player_urls(players_urls_path)

    for player_name in players_urls:
        print(f"Scrapping information on: {player_name}")

        player_details = load_player_details(
            player_data_dir + "/" + get_filename_from_player_name(player_name) + ".json"
        )
        player_id = player_details["player_id"]
        odi_matches = player_details["odi_matches"]

        odi_match_details = list()
        print(f"Number of matches: {len(odi_matches)}")
        for match in odi_matches:
            print(".", end="", sep="", flush=True)
            match_id = match["match_id"]
            match_details = get_odi_match_details(MATCH_URL.format(match_id=match_id))
            odi_match_details.append(match_details)
        print("")
        stats = dict()
        stats["player_id"] = player_id
        stats["player"] = player_name
        stats["odi_matches"] = odi_match_details

        with open(
            save_dir + f"/{get_filename_from_player_name(player_name)}.json", "w"
        ) as fp:
            json.dump(stats, fp, indent=4)
