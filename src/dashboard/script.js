// script.js

// Function to populate options for a selected player
function populatePlayerOptions(playerName) {
    const playerOptions = document.getElementById("playerOptions");
    playerOptions.innerHTML = `<h4>${playerName}</h4>
        <button class="btn btn-primary" onclick="showIntroduction('${playerName}')">Player Introduction</button>
        <button class="btn btn-primary" onclick="showBattingStatsOptions('${playerName}')">Batting Stats</button>
        <button class="btn btn-primary" onclick="showBowlingStatsOptions('${playerName}')">Bowling Stats</button>`;
    // playerOptions.style.display = "block"; // Show the options container
}

// Function to populate options for a selected team
function populateTeamOptions(teamName) {
    const playerOptions = document.getElementById("playerOptions");
    playerOptions.innerHTML = '';
    // Handle team selection logic here
    // You can add code to display team-related options
    playerOptions.innerHTML = `<h4>Optimal team for India v/s ${teamName}</h4>`;
    // playerOptions.style.display = "block"; // Show the options container
}

// Function to handle player or team selection from the dropdown
function handleSelection(dropdownType) {
    const select = dropdownType === "player" ? document.getElementById("playerSelect") : document.getElementById("teamSelect");
    const selectedValue = select.value;
    if (selectedValue) {
        // Clear existing player data and options
        document.getElementById("playerData").innerHTML = "";
        const graphContainer = document.getElementById("statsContainer");
        graphContainer.innerHTML = "";

        if (dropdownType === "player") {
            populatePlayerOptions(selectedValue);
        } else {
            populateTeamOptions(selectedValue);
        }
    }
}

// Function to display player introduction
function showIntroduction(playerName) {
    const playerData = document.getElementById("playerData");
    const graphContainer = document.getElementById("statsContainer");
    graphContainer.innerHTML = "";

    const playerIntroductions = {
        "Rohit Sharma": "Rohit Sharma is an Indian cricketer known for his elegant batting style. He is one of the best opening batsmen in the world.",
        "Hardik Pandya": "Hardik Pandya is an Indian all-rounder known for his explosive batting and effective bowling. He plays a key role in the team's success.",
        "Shubman Gill": "Shubman Gill is a young Indian cricketer who has shown great promise as a top-order batsman.",
        "Virat Kohli": "Virat Kohli is the captain of the Indian cricket team and is considered one of the best batsmen in the world.",
        "Shreyas Iyer": "Shreyas Iyer is a talented middle-order batsman known for his stylish and aggressive batting.",
        "Ishan Kishan": "Ishan Kishan is a wicketkeeper-batsman who has impressed with his aggressive batting and wicket-keeping skills.",
        "KL Rahul": "KL Rahul is a versatile cricketer known for his batting and wicket-keeping abilities.",
        "Suryakumar Yadav": "Suryakumar Yadav is a promising batsman known for his aggressive batting in the middle order.",
        "Ravindra Jadeja": "Ravindra Jadeja is an exceptional all-rounder who contributes with both bat and ball.",
        "Axar Patel": "Axar Patel is a spin-bowling all-rounder known for his tight bowling and handy batting contributions.",
        "Shardul Thakur": "Shardul Thakur is a fast bowler known for his ability to pick up crucial wickets in pressure situations.",
        "Jasprit Bumrah": "Jasprit Bumrah is India's premier fast bowler and is known for his unorthodox bowling action and deadly yorkers.",
        "Mohammed Shami": "Mohammed Shami is a key fast bowler for the Indian cricket team known for his seam and swing bowling.",
        "Mohammed Siraj": "Mohammed Siraj is a young and promising fast bowler who has shown great potential with his pace and control.",
        "Kuldeep Yadav": "Kuldeep Yadav is a left-arm chinaman bowler known for his spin variations.",
    };

    // Check if the playerName exists in playerIntroductions
    if (playerIntroductions[playerName]) {
        playerData.innerHTML = `<h4>Introduction</h4>
            <p>${playerIntroductions[playerName]}</p>
            <img src="images/${playerName.replace(' ', '_')}.jpg" alt="${playerName}" width="400" height="500">`;
    } else {
        playerData.innerHTML = `<h4>${playerName} - Introduction</h4>
            <p>Introduction not available for ${playerName}.</p>`;
    }
}

// Function to display batting stats options
function showBattingStatsOptions(playerName) {
    const graphContainer = document.getElementById("statsContainer");
    graphContainer.innerHTML = "";
    const playerData = document.getElementById("playerData");
    playerData.innerHTML = `<h4>Batting Stats</h4>
    <select onchange="showBattingGraph('${playerName}')" id="battingStatsOptions" class="form-control">
        <option selected value="Batting Average">Batting Average</option>
        <option value="Batting Strike Rate">Batting Strike Rate</option>
        <option value="Runs Scored">Runs Scored</option>
        <option value="Fifties v/s Hundreds">Fifties v/s Hundreds</option>
        <option value="Not Out Percentage">Not Out Percentage</option>
        <option value="Runs Scored at Batting Position">Runs Scored at Batting Position</option>
        <option value="Batting Strike Rate at Batting Position">Batting Strike Rate at Batting Position</option>
    </select>`
    showBattingGraph(playerName)
        // <button class="btn btn-primary" onclick="showBattingGraph('${playerName}')">Show Graph</button>`;
}

// Function to display bowling stats options
function showBowlingStatsOptions(playerName) {
    const graphContainer = document.getElementById("statsContainer");
    graphContainer.innerHTML = "";
    const playerData = document.getElementById("playerData");
    
    playerData.innerHTML = `<h4>Bowling Stats</h4>
        <select onchange="showBowlingGraph('${playerName}')" id="bowlingStatsOptions" class="form-control">
            <option value="Average Economy">Average Economy</option>
            <option value="Wickets Taken">Wickets Taken</option>
        </select>`
        // <button class="btn btn-primary" onclick="showBowlingGraph('${playerName}')">Show Graph</button>`;
    showBowlingGraph(playerName)
}

// Function to display batting graphs
function showBattingGraph(playerName) {
    const selectedOption = document.getElementById("battingStatsOptions").value;
    const graphContainer = document.getElementById("statsContainer");
    const imageName = playerName.replace(' ', '_').toLowerCase(); // Convert player name to lowercase and replace spaces with underscores

    let imagePath;

    switch (selectedOption) {
        case "Batting Average":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Batting_Averages/${imageName}_average.png`;
            break;
        case "Batting Strike Rate":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Batting_Strike_Rates/${imageName}_strike_rate.png`;
            break;
        case "Runs Scored":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Runs_Scored/${imageName}_runs.png`;
            break;
        case "Fifties v/s Hundreds":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Fifties_vs_Hundreds/${imageName}_fifties_vs_hundreds.png`;
            break;
        case "Not Out Percentage":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Not_Out_Percentages/${imageName}_not_out_percentages.png`;
            break;
        case "Runs Scored at Batting Position":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Runs_Scored_vs_Batting_Position/${imageName}_runs_scored.png`;
            break;
        case "Batting Strike Rate at Batting Position":
            imagePath = `../graph_generation/Overall_Player_Stats/Batting_Stats/Batting_Strike_Rate_vs_Batting_Position/${imageName}_strike_rate.png`;
            break;
    }

    // Display the selected graph image
    graphContainer.innerHTML = `<h5>${playerName} - ${selectedOption}</h5>
    <img src="${imagePath}" alt="${selectedOption} Graph" width="800" height="600">`;
}

// Function to display bowling graphs
function showBowlingGraph(playerName) {
    const selectedOption = document.getElementById("bowlingStatsOptions").value;
    const graphContainer = document.getElementById("statsContainer");
    const imageName = playerName.replace(' ', '_').toLowerCase(); // Convert player name to lowercase and replace spaces with underscores

    let imagePath;

    switch (selectedOption) {
        case "Average Economy":
            imagePath = `../graph_generation/Overall_Player_Stats/Bowling_Stats/Average_Economy/${imageName}_average_economy.png`;
            break;
        case "Wickets Taken":
            imagePath = `../graph_generation/Overall_Player_Stats/Bowling_Stats/Wickets_Taken/${imageName}_wickets.png`;
            break;
    }

    // Display the selected graph image
    graphContainer.innerHTML = `<h5>${playerName} - ${selectedOption}</h5>
    <img src="${imagePath}" alt="${selectedOption} Graph" width="800" height="600">`;
}


// Initialize the "Players" dropdown with player names
const playerSelect = document.getElementById("playerSelect");
const players = [
    "Rohit Sharma",
    "Hardik Pandya",
    "Shubman Gill",
    "Virat Kohli",
    "Shreyas Iyer",
    "Ishan Kishan",
    "KL Rahul",
    "Suryakumar Yadav",
    "Ravindra Jadeja",
    "Axar Patel",
    "Shardul Thakur",
    "Jasprit Bumrah",
    "Mohammed Shami",
    "Mohammed Siraj",
    "Kuldeep Yadav"
];

players.forEach((player) => {
    const option = document.createElement("option");
    option.value = player;
    option.text = player;
    playerSelect.appendChild(option);
});

// Initialize the "Optimal Team" dropdown with team names
const teamSelect = document.getElementById("teamSelect");
const teams = [
    "Australia",
    "England",
    "Pakistan",
    "New Zealand",
    "South Africa",
    "Sri Lanka",
    "Bangladesh",
    "West Indies",
    "Afghanistan"
];

teams.forEach((team) => {
    const option = document.createElement("option");
    option.value = team;
    option.text = team;
    teamSelect.appendChild(option);
});

// Add event listeners for player and team selection
playerSelect.addEventListener("change", () => {
    handleSelection("player");
    // Clear the team dropdown when a player is selected
    teamSelect.selectedIndex = 0;
});

teamSelect.addEventListener("change", () => {
    handleSelection("team");
    // Clear the player dropdown when a team is selected
    playerSelect.selectedIndex = 0;
});