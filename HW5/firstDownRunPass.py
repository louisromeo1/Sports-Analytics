# Louis Romeo
# CSC 496 HW5
# firstDownRunPass.py

import nfl_data_py as nfl
import pandas as pd
import sys

def get_input_args():
    if len(sys.argv) != 6:
        print("Usage: python firstDownRunPass.py <yardlineStart> <yardlineEnd> <timeRemaining> <WPstart> <WPend>")
        sys.exit(1)

    yardline_start = int(sys.argv[1])
    yardline_end = int(sys.argv[2])
    time_remaining = int(sys.argv[3])
    wp_start = float(sys.argv[4])
    wp_end = float(sys.argv[5])

    return yardline_start, yardline_end, time_remaining, wp_start, wp_end

def load_pbp_data(year):
    try:
        pbp_data = nfl.import_pbp_data(
            years=[year],
            columns=[
                'play_type', 'down', 'ydstogo', 'yardline_100',
                'half_seconds_remaining', 'wp', 'epa', 'posteam'
            ],
            downcast=True,
            cache=True
        )

        if pbp_data.empty:
            print(f"No data available for the {year} season.")
            sys.exit(1)

        return pbp_data

    except Exception as e:
        print(f"Failed to load data for {year}: {e}")
        sys.exit(1)

def filter_data(pbp_data, yardline_start, yardline_end, time_remaining, wp_start, wp_end):
    # Filter data based on the input criteria
    filtered_data = pbp_data[
        (pbp_data['down'] == 1) &
        (pbp_data['yardline_100'] >= yardline_start) &
        (pbp_data['yardline_100'] <= yardline_end) &
        (pbp_data['half_seconds_remaining'] > time_remaining) &
        (pbp_data['wp'] >= wp_start) &
        (pbp_data['wp'] <= wp_end) &
        (pbp_data['play_type'].isin(['run', 'pass']))
    ]

    # Exclude two-point conversion attempts
    filtered_data = filtered_data[filtered_data['ydstogo'] != 2]
    return filtered_data

def calculate_run_pass_stats(filtered_data):
    run_pass_stats = filtered_data.groupby('posteam').agg(
        total_runs=('play_type', lambda x: (x == 'run').sum()),
        total_passes=('play_type', lambda x: (x == 'pass').sum())
    )

    run_pass_stats['run_percentage'] = run_pass_stats['total_runs'] / (run_pass_stats['total_runs'] + run_pass_stats['total_passes'])
    run_pass_stats.sort_values(by='run_percentage', ascending=True, inplace=True)  # Sort by increasing run percentage

    return run_pass_stats

def print_results(run_pass_stats):
    for team, row in run_pass_stats.iterrows():
        total_runs = row['total_runs']
        total_passes = row['total_passes']
        run_percentage = row['run_percentage']
        print(f"{team} ({total_runs}, {total_passes}) {run_percentage}")

def main():
    yardline_start, yardline_end, time_remaining, wp_start, wp_end = get_input_args()

    # Load play-by-play data for 2021 season
    pbp_data = load_pbp_data(2021)

    # Filter the data based on command-line inputs
    filtered_data = filter_data(pbp_data, yardline_start, yardline_end, time_remaining, wp_start, wp_end)

    if filtered_data.empty:
        print("No data matches the filtering criteria.")
        sys.exit(1)

    # Calculate run-pass statistics for each team
    run_pass_stats = calculate_run_pass_stats(filtered_data)

    # Print results
    print_results(run_pass_stats)

if __name__ == "__main__":
    main()
