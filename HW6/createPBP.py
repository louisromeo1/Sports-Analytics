# Louis Romeo
# CSC 496 HW6
# createPBP.py

import os
import csv
import random

# Directory to store game data
output_dir = "NFLCSV"

# Fields for each play in the game data
fields = [
    "play_id", "drive_play_id_started", "half_seconds_remaining",
    "yardline_100", "down", "ydstogo", "score_differential",
    "drive_start_transition", "fixed_drive_result"
]

# Drive result options
drive_results = [
    "End of half", "Field goal", "Missed field goal", "Opp touchdown",
    "Punt", "Safety", "Touchdown", "Turnover", "Turnover on downs"
]

# Drive start transition types
drive_start_types = {0: "Turnover", 1: "Punt", 2: "Turnover on downs"}


# Function to generate random game data
def generate_game_data(game_id):
    num_plays = random.randint(50, 150)
    game_data = []
    drive_id = 0

    for play_id in range(num_plays):
        # Randomly decide if this play starts a new drive
        if play_id == 0 or random.choice([True, False]):
            drive_id = play_id
            drive_start_transition = random.choice(list(drive_start_types.keys()))
            fixed_drive_result = random.choice(drive_results)
        else:
            drive_start_transition = ""
            fixed_drive_result = ""

        # Randomly generate other fields
        play_data = {
            "play_id": play_id,
            "drive_play_id_started": drive_id,
            "half_seconds_remaining": random.randint(0, 1800),
            "yardline_100": random.randint(1, 100),
            "down": random.randint(1, 4),
            "ydstogo": random.randint(1, 10),
            "score_differential": random.randint(-21, 21),
            "drive_start_transition": drive_start_types.get(drive_start_transition, ""),
            "fixed_drive_result": fixed_drive_result
        }

        game_data.append(play_data)

    return game_data


# Function to write game data to CSV
def save_game_data(game_data, game_id):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"game_{game_id}.csv")
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for play in game_data:
            writer.writerow(play)


# Main function to generate data for multiple games
def main():
    num_games = 100  # Adjust the number of games as needed
    for game_id in range(num_games):
        game_data = generate_game_data(game_id)
        save_game_data(game_data, game_id)
        print(f"Generated data for game {game_id}")


if __name__ == "__main__":
    main()
