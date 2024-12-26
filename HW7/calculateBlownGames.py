# Louis Romeo
# CSC 496
# hw7

import os
import pandas as pd
import sys


def calculate_blown_games(directory, lower_wp_threshold, upper_wp_threshold):
    """
    Analyze games in the directory and calculate blown game statistics.

    Args:
        directory (str): Path to the directory containing CSV files.
        lower_wp_threshold (float): Lower bound of win probability threshold.
        upper_wp_threshold (float): Upper bound of win probability threshold.

    Outputs:
        Prints a table of team statistics: Games Within Thresholds, Games Won, Winning Percentage.
    """
    # Dictionary to store stats for each team
    team_stats = {}

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            # Ensure necessary columns are present
            required_columns = ['posteam', 'defteam', 'wp', 'winner']
            if not all(col in df.columns for col in required_columns):
                print(f"Skipping {filename}: Missing required columns.")
                continue

            # Track whether the game qualifies for the threshold
            game_qualifies = False
            posteam_seen = set()
            defteam_seen = set()
            game_stats = {}

            for _, row in df.iterrows():
                posteam = row['posteam']
                defteam = row['defteam']
                wp = row['wp']
                winner = row['winner']

                if pd.isna(posteam) or pd.isna(defteam) or pd.isna(wp):
                    continue

                # Check if the play falls within the win probability thresholds
                if lower_wp_threshold <= wp <= upper_wp_threshold:
                    game_qualifies = True

                    # Track stats for the offensive team
                    if posteam not in posteam_seen:
                        if posteam not in team_stats:
                            team_stats[posteam] = {'games_within_thresholds': 0, 'games_won': 0}
                        team_stats[posteam]['games_within_thresholds'] += 1
                        posteam_seen.add(posteam)
                        if posteam == winner:
                            team_stats[posteam]['games_won'] += 1

                    # Track stats for the defensive team
                    if defteam not in defteam_seen:
                        if defteam not in team_stats:
                            team_stats[defteam] = {'games_within_thresholds': 0, 'games_won': 0}
                        team_stats[defteam]['games_within_thresholds'] += 1
                        defteam_seen.add(defteam)

    # Prepare and sort results
    results = []
    for team, stats in team_stats.items():
        games_within = stats['games_within_thresholds']
        games_won = stats['games_won']
        winning_percentage = (games_won / games_within) * 100 if games_within > 0 else 0
        results.append((team, games_within, games_won, winning_percentage))

    # Sort results by Winning Percentage (Descending)
    results.sort(key=lambda x: x[3], reverse=True)

    # Print results in requested format
    print("Team, Games Within Thresholds, Games Won, Winning Percentage")
    for team, games_within, games_won, winning_percentage in results:
        print(f"{team}, {games_within}, {games_won}, {winning_percentage:.2f}%")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python calculateBlownGames.py <directory> <lowerWPThreshold> <upperWPThreshold>")
        sys.exit(1)

    directory = sys.argv[1]
    lower_wp_threshold = float(sys.argv[2])
    upper_wp_threshold = float(sys.argv[3])

    calculate_blown_games(directory, lower_wp_threshold, upper_wp_threshold)
