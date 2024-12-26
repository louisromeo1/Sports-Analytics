# Louis Romeo
# CSC 496 HW4
# hitDistanceAnalysis.py

import sys
import pandas as pd

# Check for input CSV files
if len(sys.argv) < 3:
    print("Usage: python hitDistanceAnalysis.py <pull_file> <oppo_file>")
    sys.exit(1)

# Load the data
pull_file = sys.argv[1]
oppo_file = sys.argv[2]
pull_data = pd.read_csv(pull_file)
oppo_data = pd.read_csv(oppo_file)

# Ensure the necessary column 'hit_distance_sc' is present
if 'hit_distance_sc' not in pull_data.columns or 'hit_distance_sc' not in oppo_data.columns:
    print("Error: Missing column 'hit_distance_sc' in one of the input files.")
    sys.exit(1)

# Filter for fly balls (assume fly balls have launch_angle > 20 degrees)
pull_fly_balls = pull_data[pull_data['launch_angle'] > 20]
oppo_fly_balls = oppo_data[oppo_data['launch_angle'] > 20]

# Calculate total number of fly balls and average distances
total_fly_balls = len(pull_fly_balls) + len(oppo_fly_balls)
num_pull_fly_balls = len(pull_fly_balls)
avg_distance_pull = pull_fly_balls['hit_distance_sc'].mean() if num_pull_fly_balls > 0 else 0
num_oppo_fly_balls = len(oppo_fly_balls)
avg_distance_oppo = oppo_fly_balls['hit_distance_sc'].mean() if num_oppo_fly_balls > 0 else 0

# Output the results
print(total_fly_balls)
print(num_pull_fly_balls)
print(avg_distance_pull)
print(num_oppo_fly_balls)
print(avg_distance_oppo)
