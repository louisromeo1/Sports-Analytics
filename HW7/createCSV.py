# Louis Romeo
# CSC 496
# hw7
import os
import pandas as pd
import nfl_data_py as nfl

def save_csv_files(start_year, end_year, output_dir):
    """
    Saves play-by-play data as individual game CSV files for each year in the given range.
        start_year (int): Starting year of the data.
        end_year (int): Ending year of the data.
        output_dir (str): Directory where the CSV files will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for season in range(start_year, end_year + 1):
        print(f"Processing season {season}...")

        # Load play-by-play data for the season
        pbp_data = nfl.import_pbp_data([season])

        # Filter the necessary columns
        required_columns = [
            'posteam', 'defteam', 'wp', 'score_differential_post', 'home_team',
            'away_team', 'home_score', 'away_score', 'play_id', 'game_id'
        ]
        pbp_data = pbp_data[required_columns].dropna()

        # Determine the winner of each game
        winners = {}
        for game_id in pbp_data['game_id'].unique():
            game_data = pbp_data[pbp_data['game_id'] == game_id]
            final_play = game_data.iloc[-1]
            home_team = final_play['home_team']
            away_team = final_play['away_team']
            home_score = final_play['home_score']
            away_score = final_play['away_score']
            winner = home_team if home_score > away_score else away_team
            winners[game_id] = winner

        # Add the "winner" column to the DataFrame
        pbp_data['winner'] = pbp_data['game_id'].map(winners)

        # Save each game's data as a separate CSV file
        for game_id in pbp_data['game_id'].unique():
            game_data = pbp_data[pbp_data['game_id'] == game_id]
            output_file = os.path.join(output_dir, f"{game_id}.csv")
            game_data.to_csv(output_file, index=False)
            print(f"Saved {output_file}")

if __name__ == "__main__":
    # Set parameters
    START_YEAR = 2001
    END_YEAR = 2023
    OUTPUT_DIR = "NFLCSV"

    # Call the function to save CSV files
    save_csv_files(START_YEAR, END_YEAR, OUTPUT_DIR)
