import csv
import os

# Louis Romeo
# CSC 496 HW2

# File to track the processed games and winners
OUTPUT_FILE = 'hw2.csv'


# Function to extract base occupancy
def get_base_occupancy(runners):
    """Returns binary flags for first, second, and third base occupancy."""
    return ('1' if '1' in runners else '0',
            '1' if '2' in runners else '0',
            '1' if '3' in runners else '0')


# Function to calculate run differential
def calculate_run_differential(score, team_at_bat):
    home_score, away_score = map(int, score.split('-'))
    return home_score - away_score if team_at_bat == "home" else away_score - home_score


# Process each play and generate the six-entry format
def process_game_data(team, plays, winner_team):
    total_outs = 0
    win_flag = 1 if winner_team == team else 0
    run_diff = 0
    base_occupancy = ('0', '0', '0')  # Base occupancy flags (first, second, third)

    output_rows = []

    for play in plays:
        inning, score, outs, runners, pitch_code, wp_change, current_wp, batter, pitcher, description = play

        # Calculate total outs (outs + (3 * inning) if top or bottom)
        if 'b' in inning:
            total_outs = (int(inning[1:]) - 1) * 6 + int(outs) + 3  # Bottom of inning
        else:
            total_outs = (int(inning[1:]) - 1) * 6 + int(outs)  # Top of inning

        # Get current base occupancy
        base_occupancy = get_base_occupancy(runners)

        # Calculate run differential
        run_diff = calculate_run_differential(score, 'home' if 'b' in inning else 'away')

        # Prepare the data row for the play (before the play is completed)
        row = [total_outs, run_diff] + list(base_occupancy) + [win_flag]
        output_rows.append(row)

        # Update run differential after the play
        # Assuming the description contains the play outcome, update the score manually (e.g., for triples, home runs, etc.)
        if "Triple" in description:
            run_diff += 2  # Two runs score for the example given

        # Update base occupancy if runners moved due to the play
        if "Triple" in description:
            base_occupancy = ('0', '0', '1')  # Runner ends up on third after triple

        # Prepare the data row after the play
        row = [total_outs, run_diff] + list(base_occupancy) + [win_flag]
        output_rows.append(row)

    return output_rows


# Save the data to a CSV
def save_to_csv(output_rows):
    with open(OUTPUT_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)


# Determine the winner of the game
def determine_winner(plays):
    last_play = plays[-1]
    inning, score, _, _, _, _, _, _, _, _ = last_play
    home_score, away_score = map(int, score.split('-'))

    if 'b9' not in inning:  # No bottom of the 9th, away team wins
        return 'away'
    elif home_score > away_score:  # Home team batted in 9th and won
        return 'home'
    else:
        return 'away'


# Main function to process the game and generate the win probability data
def process_game(team, game_plays):
    winner_team = determine_winner(game_plays)
    game_data = process_game_data(team, game_plays, winner_team)
    save_to_csv(game_data)


# Example usage with dummy data for a single game
game_plays = [
    # inning, score, outs, runners, pitch_code, wp_change, current_wp, batter, pitcher, description
    ('b5', '2-4', '2', '1-3', 'TF1 X', '-25%', '45%', 'Jason Vosler', 'Mitch Keller', 'Triple to RF'),
    # Add more plays from the game here...
]

# Process the game for team CIN
process_game('CIN', game_plays)
