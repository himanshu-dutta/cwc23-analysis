import json
import os
import plotly.express as px

output_directory = os.path.abspath("./Batting Strike Rates")
os.makedirs(output_directory, exist_ok=True)

json_file_path = os.path.abspath("../../data/players.json")

with open(json_file_path, 'r') as json_file:
    player_data = json.load(json_file)

players = [player_name.replace(" ", "_").lower() for player_name in player_data.keys()]

for player_name in players:
    parent_directory = os.path.join("..", "..")
    json_file_path = os.path.join(parent_directory, "data/players", f"{player_name}.json")

    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    batting_strike_rates = []
    years = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                btsr = stat["btsr"]
                if year >= 2017 and btsr is not None:
                    years.append(year)
                    batting_strike_rates.append(float(btsr))

    player_title = player_name.replace('_', ' ').title()
    fig = px.line(x=years, y=batting_strike_rates, labels={"x": "Year", "y": "Batting Strike Rate"})
    fig.update_layout(title=f"{player_title}'s Batting Strike Rate Over the Years (2017 or Beyond)")

    image_file_path = os.path.join(output_directory, f"{player_name}.png")
    fig.write_image(image_file_path)

print("Graphs saved in the '../Batting Strike Rates' folder.")
