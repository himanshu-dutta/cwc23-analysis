import json
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import defaultdict

# terminolofy mapping for extracting data from json files
terminology_mapping = {
    "tt": "type",
    "sp": "span",
    "mt": "matches",
    "in": "innings",
    "pr": None,
    "rn": "runs",
    "fo": "fours",
    "si": "sixes",
    "ft": "fifties",
    "hn": "hundreds",
    "bf": "balls_faced",
    "dk": "ducks",
    "no": "not_outs",
    "hs": "high_score",
    "bta": "batting_average",
    "btsr": "batting_strike_rate",
    "wk": "wickets_taken",
    "bwe": "average_economy",
    "md": "maiden_overs",
    "bwsr": "bowling_strike_rate",
    "ov": "overs_bowled"
}

# function for batting strike rate vs batting position graph
def generate_batting_strike_rate_vs_batting_position_graph(data, output_directory, player_name):
    batting_positions = []
    batting_strike_rates = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "BATTING_POSITION":
            for stat in stats_group["stats"]:
                position = stat["tt"] 
                batting_positions.append(position)
                batting_strike_rates.append(float(stat["btsr"]))

    custom_order = ["1st position", "2nd position", "3rd position", "4th position", "5th position", "6th position", "7th position", "8th position", "9th position", "10th position", "11th position"]

    player_title = player_name.replace('_', ' ').title()
    df = pd.DataFrame({
        "Batting Position": batting_positions,
        "Batting Strike Rate": batting_strike_rates
    })

    df["Batting Position"] = pd.Categorical(df["Batting Position"], categories=custom_order, ordered=True)
    df = df.sort_values("Batting Position")

    fig = px.bar(df, x="Batting Position", y="Batting Strike Rate", color="Batting Strike Rate", title=f"{player_title}'s Batting Strike Rate at Batting Position")
    image_file_path = os.path.join(output_directory, f"{player_name}_strike_rate.png")
    fig.write_image(image_file_path)

# function for runs scored vs batting position graph
def generate_runs_scored_vs_batting_position_graph(data, output_directory, player_name):
    batting_positions = []
    runs_scored = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "BATTING_POSITION":
            for stat in stats_group["stats"]:
                position = stat["tt"]  
                batting_positions.append(position)
                runs_scored.append(int(stat["rn"])) 

    custom_order = ["1st position", "2nd position", "3rd position", "4th position", "5th position", "6th position", "7th position", "8th position", "9th position", "10th position", "11th position"]

    player_title = player_name.replace('_', ' ').title()
    df = pd.DataFrame({
        "Batting Position": batting_positions,
        "Runs Scored": runs_scored
    })

    df["Batting Position"] = pd.Categorical(df["Batting Position"], categories=custom_order, ordered=True)
    df = df.sort_values("Batting Position")

    fig = px.bar(df, x="Batting Position", y="Runs Scored", color="Runs Scored", title=f"{player_title}'s Runs Scored at Batting Position")
    image_file_path = os.path.join(output_directory, f"{player_name}_runs_scored.png")
    fig.write_image(image_file_path)

# function for generating not out percentages
def generate_not_out_percentages_graph(player_data, output_directory, player_name):
    odi_matches = player_data.get("odi_matches", [])
    not_out_counts = defaultdict(int)
    match_counts = defaultdict(int)

    for match in odi_matches:
        match_date = match["date"]
        match_year = int(match_date.split()[-1])
        if 2017 <= match_year:
            not_out_counts[match_year] += int(match["not_out"])
            match_counts[match_year] += 1

    years = list(not_out_counts.keys())
    not_out_percentages = [100 * not_out_counts[year] / match_counts[year] if match_counts[year] > 0 else 0 for year in years]

    player_title = player_name.replace('_', ' ').title()
    df = pd.DataFrame({
        "Year": years,
        "Not Out Percentage": not_out_percentages
    })

    fig = px.bar(df, x="Year", y="Not Out Percentage", labels={"x": "Year", "y": "Not Out Percentage"})
    fig.update_layout(title=f"{player_title}'s Not Out Percentage Over the Years (2017 and Beyond)")
    fig.update_yaxes(range=[0, 100])
    fig.update_xaxes(tickvals=years)
    image_file_path_not_out_percentages = os.path.join(output_directory, f"{player_name}_not_out_percentages.png")
    fig.write_image(image_file_path_not_out_percentages)

# function for generating batting strike rate graph
def generate_batting_strike_rate_graph(data, output_directory, player_name):
    years = []
    batting_strike_rates = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                year_data["Year"] = year
                if year >= 2017 and year_data["batting_strike_rate"] is not None:
                    years.append(year)
                    batting_strike_rates.append(float(year_data["batting_strike_rate"]))

    player_title = player_name.replace('_', ' ').title()
    df_strike_rate = pd.DataFrame({
        "Year": years,
        "Batting Strike Rate": batting_strike_rates
    })

    fig_strike_rate = px.line(df_strike_rate, x="Year", y="Batting Strike Rate", labels={"x": "Year", "y": "Batting Strike Rate"})
    fig_strike_rate.update_layout(title=f"{player_title}'s Batting Strike Rate Over the Years (2017 and Beyond)")
    fig_strike_rate.update_xaxes(tickvals=years)
    image_file_path_strike_rate = os.path.join(output_directory, f"{player_name}_strike_rate.png")
    fig_strike_rate.write_image(image_file_path_strike_rate)

# function for generating batting average graph
def generate_batting_average_graph(data, output_directory, player_name):
    years = []
    batting_averages = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                year_data["Year"] = year
                if year >= 2017 and year_data["batting_average"] is not None:
                    years.append(year)
                    batting_averages.append(float(year_data["batting_average"]))

    player_title = player_name.replace('_', ' ').title()
    df_average = pd.DataFrame({
        "Year": years,
        "Batting Average": batting_averages
    })

    fig_average = px.line(df_average, x="Year", y="Batting Average", labels={"x": "Year", "y": "Batting Average"})
    fig_average.update_layout(title=f"{player_title}'s Batting Average Over the Years (2017 and Beyond)")
    fig_average.update_xaxes(tickvals=years)
    image_file_path_average = os.path.join(output_directory, f"{player_name}_average.png")
    fig_average.write_image(image_file_path_average)

# function for generating runs scored graph
def generate_runs_scored_graph(data, output_directory, player_name):
    years = []
    runs_scored = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                year_data["Year"] = year
                if year >= 2017 and year_data["runs"] is not None:
                    years.append(year)
                    runs_scored.append(int(year_data["runs"]))

    player_title = player_name.replace('_', ' ').title()
    df_runs = pd.DataFrame({
        "Year": years,
        "Runs Scored": runs_scored
    })

    fig_runs = px.scatter(df_runs, x="Year", y="Runs Scored", size="Runs Scored", color="Runs Scored", labels={"x": "Year", "y": "Runs Scored"})
    fig_runs.update_layout(title=f"{player_title}'s Runs Scored Over the Years (2017 and Beyond)")
    fig_runs.update_xaxes(tickvals=years)
    image_file_path_runs = os.path.join(output_directory, f"{player_name}_runs.png")
    fig_runs.write_image(image_file_path_runs)

# functions for generating fifties vs hundreds graph
def generate_fifties_vs_hundreds_graph(data, output_directory, player_name):
    years = []
    fifties = []
    hundreds = []

    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                year_data["Year"] = year
                if year >= 2017 and year_data["fifties"] is not None and year_data["hundreds"] is not None:
                    years.append(year)
                    fifties.append(int(year_data["fifties"]))
                    hundreds.append(int(year_data["hundreds"]))

    player_title = player_name.replace('_', ' ').title()
    df_fifties_vs_hundreds = pd.DataFrame({
        "Year": years,
        "50s": fifties,
        "100s": hundreds
    })

    fig_fifties_vs_hundreds = px.bar(df_fifties_vs_hundreds, x="Year", y=["50s", "100s"],
                                      labels={"x": "Year", "value": "Count"}, barmode="group")
    fig_fifties_vs_hundreds.update_layout(title=f"{player_title}'s 50s vs 100s Over the Years (2017 and Beyond)")
    fig_fifties_vs_hundreds.update_xaxes(tickvals=years)
    image_file_path_fifties_vs_hundreds = os.path.join(output_directory, f"{player_name}_fifties_vs_hundreds.png")
    fig_fifties_vs_hundreds.write_image(image_file_path_fifties_vs_hundreds)

# function for generating wickets taken graph
def generate_wickets_taken_graph(data, output_directory, player_name):
    years = []
    wickets_taken = []

    for stats_group in data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                if year >= 2017:  # Filter data for years 2017 and beyond
                    year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                    year_data["Year"] = year
                    if year_data["wickets_taken"] is not None:
                        years.append(year)
                        wickets_taken.append(int(year_data["wickets_taken"]))

    player_title = player_name.replace('_', ' ').title()
    df_wickets = pd.DataFrame({
        "Year": years,
        "Wickets Taken": wickets_taken
    })

    fig_wickets = px.bar(df_wickets, x="Year", y="Wickets Taken", color="Wickets Taken", labels={"x": "Year", "y": "Wickets Taken"})
    fig_wickets.update_layout(title=f"{player_title}'s Wickets Taken Over the Years (2017 and Beyond)")
    fig_wickets.update_xaxes(title_text=None)
    fig_wickets.update_xaxes(tickvals=years)  
    fig_wickets.add_annotation(
        text="Year",
        x=0.5,
        y=-0.1,
        xref="paper",
        yref="paper",
        showarrow=False
    )
    image_file_path_wickets = os.path.join(output_directory, f"{player_name}_wickets.png")
    fig_wickets.write_image(image_file_path_wickets)

# function for generating average economy graph
def generate_average_economy_graph(data, output_directory, player_name):
    years = []
    average_economy = []

    for stats_group in data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                if year >= 2017:  # Filter data for years 2017 and beyond
                    year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                    year_data["Year"] = year
                    if year_data["average_economy"] is not None:
                        years.append(year)
                        average_economy.append(float(year_data["average_economy"]))

    player_title = player_name.replace('_', ' ').title()
    df_average_economy = pd.DataFrame({
        "Year": years,
        "Average Economy": average_economy
    })

    fig_average_economy = px.line(df_average_economy, x="Year", y="Average Economy", labels={"x": "Year", "y": "Average Economy"})
    fig_average_economy.update_layout(title=f"{player_title}'s Average Economy Over the Years (2017 and Beyond)")
    fig_average_economy.update_xaxes(title_text=None)
    fig_average_economy.update_xaxes(tickvals=years) 
    fig_average_economy.add_annotation(
        text="Year",
        x=0.5,
        y=-0.1,
        xref="paper",
        yref="paper",
        showarrow=False
    )
    image_file_path_average_economy = os.path.join(output_directory, f"{player_name}_average_economy.png")
    fig_average_economy.write_image(image_file_path_average_economy)

# function for generating maiden overs graph
def generate_maiden_overs_graph(data, output_directory, player_name):
    years = []
    maiden_overs = []

    for stats_group in data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                if year >= 2017:  # Filter data for years 2017 and beyond
                    year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                    year_data["Year"] = year
                    if year_data["maiden_overs"] is not None:
                        years.append(year)
                        maiden_overs.append(int(year_data["maiden_overs"]))

    player_title = player_name.replace('_', ' ').title()
    df_maiden_overs = pd.DataFrame({
        "Year": years,
        "Maiden Overs": maiden_overs
    })

    fig_maiden_overs = px.line(df_maiden_overs, x="Year", y="Maiden Overs", labels={"x": "Year", "y": "Maiden Overs"})
    fig_maiden_overs.update_layout(title=f"{player_title}'s Maiden Overs Over the Years (2017 and Beyond)")
    fig_maiden_overs.update_xaxes(title_text=None)
    fig_maiden_overs.update_xaxes(tickvals=years)
    fig_maiden_overs.add_annotation(
        text="Year",
        x=0.5,
        y=-0.1,
        xref="paper",
        yref="paper",
        showarrow=False
    )
    image_file_path_maiden_overs = os.path.join(output_directory, f"{player_name}_maiden_overs.png")
    fig_maiden_overs.write_image(image_file_path_maiden_overs)

# function for generating bowling strike rate graph
def generate_bowling_strike_rate_graph(data, output_directory, player_name):
    years = []
    bowling_strike_rates = []

    for stats_group in data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                if year >= 2017:  # Filter data for years 2017 and beyond
                    year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                    year_data["Year"] = year
                    if year_data["bowling_strike_rate"] is not None:
                        years.append(year)
                        bowling_strike_rates.append(float(year_data["bowling_strike_rate"]))

    player_title = player_name.replace('_', ' ').title()
    df_bowling_strike_rate = pd.DataFrame({
        "Year": years,
        "Bowling Strike Rate": bowling_strike_rates
    })

    fig_bowling_strike_rate = px.line(df_bowling_strike_rate, x="Year", y="Bowling Strike Rate", labels={"x": "Year", "y": "Bowling Strike Rate"})
    fig_bowling_strike_rate.update_layout(title=f"{player_title}'s Bowling Strike Rate Over the Years (2017 and Beyond)")
    fig_bowling_strike_rate.update_xaxes(title_text=None)
    fig_bowling_strike_rate.update_xaxes(tickvals=years)
    fig_bowling_strike_rate.add_annotation(
        text="Year",
        x=0.5,
        y=-0.1,
        xref="paper",
        yref="paper",
        showarrow=False
    )
    image_file_path_bowling_strike_rate = os.path.join(output_directory, f"{player_name}_bowling_strike_rate.png")
    fig_bowling_strike_rate.write_image(image_file_path_bowling_strike_rate)

# function for generating overs bowled graph
def generate_overs_bowled_graph(data, output_directory, player_name):
    years = []
    total_overs_bowled = []

    for stats_group in data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "YEAR":
            for stat in stats_group["stats"]:
                year = int(stat["tt"].split()[-1])
                if year >= 2017:  # Filter data for years 2017 and beyond
                    year_data = {terminology_mapping[key]: value for key, value in stat.items() if key in terminology_mapping}
                    year_data["Year"] = year
                    if year_data["overs_bowled"] is not None:
                        years.append(year)
                        total_overs_bowled.append(float(year_data["overs_bowled"]))

    player_title = player_name.replace('_', ' ').title()
    labels = [f"{year} ({overs} overs)" for year, overs in zip(years, total_overs_bowled)]
    fig_overs_bowled = go.Figure(data=[go.Pie(labels=labels, values=total_overs_bowled)])
    fig_overs_bowled.update_layout(title=f"{player_title}'s Total Overs Bowled Over the Years (2017 and Beyond)")
    image_file_path_overs_bowled = os.path.join(output_directory, f"{player_name}_overs_bowled.png")
    fig_overs_bowled.write_image(image_file_path_overs_bowled)

# function for generating runs scored against individual teams graph
def generate_runs_scored_against_individual_teams_graph(player_data, output_directory, player_name):
    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "OPPOSITION_TEAM":
            opposition_data = stats_group.get("stats", [])
            break

    runs_data = []
    for opposition in opposition_data:
        opposition_name = opposition.get("tt", "")
        if(opposition_name in ["vs Australia", "vs England", "vs Pakistan", "vs New Zealand", "vs Sri Lanka", "vs Bangladesh", "vs West Indies", "vs Afghanistan"]):
            runs_data.append({
                "Opposition": opposition_name,
                "Runs Scored": opposition.get("rn", 0),
            })

    df = pd.DataFrame(runs_data)
    fig = px.bar(df, x="Opposition", y="Runs Scored", color="Runs Scored", labels={"x": "Opposition Team", "y": "Runs Scored"})
    
    player_title = player_name.replace('_', ' ').title()
    fig.update_layout(title=f"{player_title}'s Runs Scored Against Individial Teams")
    image_file_path_runs_scored_against_individual_teams = os.path.join(output_directory, f"{player_name}_runs_scored_against_individual_teams.png")
    fig.write_image(image_file_path_runs_scored_against_individual_teams)

# function for generating batting strike rate against individual teams 
def generate_batting_strike_rate_against_individual_teams_graph(player_data, output_directory, player_name):
    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "OPPOSITION_TEAM":
            opposition_data = stats_group.get("stats", [])
            break

    runs_data = []
    for opposition in opposition_data:
        opposition_name = opposition.get("tt", "")
        if(opposition_name in ["vs Australia", "vs England", "vs Pakistan", "vs New Zealand", "vs Sri Lanka", "vs Bangladesh", "vs West Indies", "vs Afghanistan"]):
            runs_data.append({
                "Opposition": opposition_name,
                "Batting Strike Rate": opposition.get("btsr", 0),
            })

    df = pd.DataFrame(runs_data)
    fig = px.bar(df, x="Opposition", y="Batting Strike Rate",color="Batting Strike Rate", labels={"x": "Opposition Team", "y": "Batting Strike Rate"})
    
    player_title = player_name.replace('_', ' ').title()
    fig.update_layout(title=f"{player_title}'s Batting Strike Rate Against Individial Teams")
    image_file_path_batting_strike_rate_against_individual_teams = os.path.join(output_directory, f"{player_name}_batting_strike_rate_against_individual_teams.png")
    fig.write_image(image_file_path_batting_strike_rate_against_individual_teams)

# function for generating not our percentages against individual teams graph
def generate_not_out_percentages_against_individual_team_graph(player_data, output_directory, player_name):
    for stats_group in data["BATTING"]["summary"]["groups"]:
        if stats_group["type"] == "OPPOSITION_TEAM":
            opposition_data = stats_group.get("stats", [])
            break

    runs_data = []
    for opposition in opposition_data:
        opposition_name = opposition.get("tt", "")
        if(opposition_name in ["vs Australia", "vs England", "vs Pakistan", "vs New Zealand", "vs Sri Lanka", "vs Bangladesh", "vs West Indies", "vs Afghanistan"]):
            runs_data.append({
                "Opposition": opposition_name,
                "Not Outs": opposition.get("no", 0),
                "Total Matches": opposition.get("mt", 0),
            })

    df = pd.DataFrame(runs_data)
    df["Not Out Percentages"] = (df["Not Outs"] / df["Total Matches"]) * 100 
    player_title = player_name.replace('_', ' ').title()
    fig = px.pie(df, names="Opposition", values="Not Out Percentages", title=f"{player_title}'s Not Out Percentages Against Individual Teams")
    image_file_path_batting_strike_rate_against_individual_teams = os.path.join(output_directory, f"{player_name}_not_out_percentages_against_individual_teams.png")
    fig.write_image(image_file_path_batting_strike_rate_against_individual_teams)

# function for generating wickets taken against individuyal teams graph
def generate_wickets_taken_against_individual_teams_graph(player_data, output_directory, player_name):
    opposition_data = None

    for stats_group in player_data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "OPPOSITION_TEAM":
            opposition_data = stats_group.get("stats", [])
            break

    runs_data = []
    for opposition in opposition_data:
        opposition_name = opposition.get("tt", "")
        if opposition_name in ["vs Australia", "vs England", "vs Pakistan", "vs New Zealand", "vs Sri Lanka", "vs Bangladesh", "vs West Indies", "vs Afghanistan"]:
            runs_data.append({
                "Opposition": opposition_name,
                "Wickets": opposition.get("wk", 0),
            })

    df = pd.DataFrame(runs_data)
    df = df.dropna(subset=["Wickets"])
    
    player_title = player_name.replace('_', ' ').title()
    fig = px.scatter(df, x="Opposition", y="Wickets", size="Wickets", color="Wickets", title=f"{player_title}'s Wickets Against Individual Teams")
    image_file_path_wickets_taken_against_individual_teams = os.path.join(output_directory, f"{player_name}_wickets_taken_against_individual_teams.png")
    fig.write_image(image_file_path_wickets_taken_against_individual_teams)

# functions for generating average economy against individual teams graph
def generate_average_economy_against_individual_teams_graph(player_data, output_directory, player_name):
    opposition_data = None
    for stats_group in player_data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "OPPOSITION_TEAM":
            opposition_data = stats_group.get("stats", [])
            break

    bowling_economy_data = []
    for opposition in opposition_data:
        opposition_name = opposition.get("tt", "")
        if opposition_name in ["vs Australia", "vs England", "vs Pakistan", "vs New Zealand", "vs Sri Lanka", "vs Bangladesh", "vs West Indies", "vs Afghanistan"]:
            bowling_economy_data.append({
                "Opposition": opposition_name,
                "Average Economy": opposition.get("bwe", 0),
            })

    df = pd.DataFrame(bowling_economy_data)

    # Drop rows with NaN values in the "Average Economy" column
    df = df.dropna(subset=["Average Economy"])
    player_title = player_name.replace('_', ' ').title()
    fig = px.bar(df, x="Opposition", y="Average Economy", color="Average Economy", title=f"{player_title}'s Average Economy Against Individual Teams")
    image_file_path_average_economy_against_individual_teams = os.path.join(output_directory, f"{player_name}_average_economy_against_individual_teams.png")
    fig.write_image(image_file_path_average_economy_against_individual_teams)

# function for generating bowling strike rate against individual teams graph
def generate_bowling_strike_rate_against_individual_teams_graph(player_data, output_directory, player_name):
    opposition_data = None

    for stats_group in player_data["BOWLING"]["summary"]["groups"]:
        if stats_group["type"] == "OPPOSITION_TEAM":
            opposition_data = stats_group.get("stats", [])
            break

    bowling_strike_rate = []
    for opposition in opposition_data:
        opposition_name = opposition.get("tt", "")
        if opposition_name in ["vs Australia", "vs England", "vs Pakistan", "vs New Zealand", "vs Sri Lanka", "vs Bangladesh", "vs West Indies", "vs Afghanistan"]:
            bowling_strike_rate.append({
                "Opposition": opposition_name,
                "Bowling Strike Rate": opposition.get("bwsr", 0),
            })

    df = pd.DataFrame(bowling_strike_rate)

    # Drop rows with NaN values in the "Bowling Strike Rate" column
    df = df.dropna(subset=["Bowling Strike Rate"])
    player_title = player_name.replace('_', ' ').title()
    fig = px.bar(df, x="Opposition", y="Bowling Strike Rate", color="Bowling Strike Rate", title=f"{player_title}'s Bowling Strike Rate Against Individual Teams")
    image_file_path_bowling_strike_rate_against_individual_teams = os.path.join(output_directory, f"{player_name}_bowling_strike_rate_against_individual_teams.png")
    fig.write_image(image_file_path_bowling_strike_rate_against_individual_teams)

output_directory_strike_rates = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Batting_Strike_Rates")
output_directory_averages = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Batting_Averages")
output_directory_runs = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Runs_Scored")
output_directory_fifties_vs_hundreds = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Fifties_vs_Hundreds")
output_directory_not_out_percentages = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Not_Out_Percentages")
output_directory_generate_runs_scored_vs_batting_position = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Runs_Scored_vs_Batting_Position")
output_directory_generate_batting_strike_rate_vs_batting_position = os.path.abspath("./Overall_Player_Stats/Batting_Stats/Batting_Strike_Rate_vs_Batting_Position")
output_directory_wickets_taken = os.path.abspath("./Overall_Player_Stats/Bowling_Stats/Wickets_Taken")
output_directory_average_economy = os.path.abspath("./Overall_Player_Stats/Bowling_Stats/Average_Economy")
output_directory_maiden_overs = os.path.abspath("./Overall_Player_Stats/Bowling_Stats/Maiden_Overs")
output_directory_bowling_strike_rate = os.path.abspath("./Overall_Player_Stats/Bowling_Stats/Bowling_Strike_Rate")
output_directory_overs_bowled = os.path.abspath("./Overall_Player_Stats/Bowling_Stats/Overs_Bowled")
output_directory_runs_scored_against_individual_teams = os.path.abspath("./Vs_Other_Teams/Runs_Scored_Against_Individual_Teams")
output_directory_batting_strike_rate_against_individual_teams = os.path.abspath("./Vs_Other_Teams/Batting_Strike_Rate_Against_Individual_Teams")
output_directory_not_out_percentages_againt_individual_teams = os.path.abspath("./Vs_Other_Teams/Not_Out_Percentages_Against_Individual_Teams")
output_directory_wickets_taken_against_individual_teams = os.path.abspath("./Vs_Other_Teams/Wickets_Taken_Against_Individual_Teams")
output_directory_average_economy_against_individual_teams = os.path.abspath("./Vs_Other_Teams/Average_Economy_Against_Individual_Teams")
output_directory_bowling_strike_rate_against_individual_teams = os.path.abspath("./Vs_Other_Teams/Bowling_Strike_Rate_Against_Individual_Teams")

os.makedirs(output_directory_strike_rates, exist_ok=True)
os.makedirs(output_directory_averages, exist_ok=True)
os.makedirs(output_directory_runs, exist_ok=True)
os.makedirs(output_directory_fifties_vs_hundreds, exist_ok=True)
os.makedirs(output_directory_not_out_percentages, exist_ok=True)
os.makedirs(output_directory_generate_runs_scored_vs_batting_position, exist_ok=True)
os.makedirs(output_directory_generate_batting_strike_rate_vs_batting_position, exist_ok=True)
os.makedirs(output_directory_wickets_taken, exist_ok=True)
os.makedirs(output_directory_average_economy, exist_ok=True)
os.makedirs(output_directory_maiden_overs, exist_ok=True)
os.makedirs(output_directory_bowling_strike_rate, exist_ok=True)
os.makedirs(output_directory_overs_bowled, exist_ok=True)
os.makedirs(output_directory_runs_scored_against_individual_teams, exist_ok=True)
os.makedirs(output_directory_batting_strike_rate_against_individual_teams, exist_ok=True)
os.makedirs(output_directory_not_out_percentages_againt_individual_teams, exist_ok=True)
os.makedirs(output_directory_wickets_taken_against_individual_teams, exist_ok=True)
os.makedirs(output_directory_average_economy_against_individual_teams, exist_ok=True)
os.makedirs(output_directory_bowling_strike_rate_against_individual_teams, exist_ok=True)

json_file_path = os.path.abspath("../../data/players.json")

with open(json_file_path, 'r') as json_file:
    player_data = json.load(json_file)

players = [player_name.replace(" ", "_").lower() for player_name in player_data.keys()]

for player_name in players:
    parent_directory = os.path.join("..", "..")
    json_file_path = os.path.join(parent_directory, "data/players", f"{player_name}.json")

    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    generate_not_out_percentages_graph(data, output_directory_not_out_percentages, player_name)
    generate_batting_strike_rate_graph(data, output_directory_strike_rates, player_name)
    generate_batting_average_graph(data, output_directory_averages, player_name)
    generate_runs_scored_graph(data, output_directory_runs, player_name)
    generate_fifties_vs_hundreds_graph(data, output_directory_fifties_vs_hundreds, player_name)
    generate_runs_scored_vs_batting_position_graph(data, output_directory_generate_runs_scored_vs_batting_position, player_name)
    generate_batting_strike_rate_vs_batting_position_graph(data, output_directory_generate_batting_strike_rate_vs_batting_position, player_name)
    generate_wickets_taken_graph(data, output_directory_wickets_taken, player_name)
    generate_average_economy_graph(data, output_directory_average_economy, player_name)
    generate_maiden_overs_graph(data, output_directory_maiden_overs, player_name)
    generate_bowling_strike_rate_graph(data, output_directory_bowling_strike_rate, player_name)
    generate_overs_bowled_graph(data, output_directory_overs_bowled, player_name)
    generate_runs_scored_against_individual_teams_graph(data, output_directory_runs_scored_against_individual_teams, player_name)
    generate_batting_strike_rate_against_individual_teams_graph(data, output_directory_batting_strike_rate_against_individual_teams, player_name)
    generate_not_out_percentages_against_individual_team_graph(data, output_directory_not_out_percentages_againt_individual_teams, player_name)
    generate_wickets_taken_against_individual_teams_graph(data, output_directory_wickets_taken_against_individual_teams, player_name)
    generate_average_economy_against_individual_teams_graph(data, output_directory_average_economy_against_individual_teams, player_name)
    generate_bowling_strike_rate_against_individual_teams_graph(data, output_directory_bowling_strike_rate_against_individual_teams, player_name)

print("Graphs saved in their respective folders.")