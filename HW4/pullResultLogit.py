# Louis Romeo
# CSC 496 HW4
# pullResultLogit.py
import sys
import pandas as pd

# Check for input CSV file
if len(sys.argv) < 2:
    print("Usage: python pullResultLogit.py <input_file>")
    sys.exit(1)

# Load the data
input_file = sys.argv[1]
data = pd.read_csv(input_file)

# Ensure necessary column 'woba_value' is present
if 'woba_value' not in data.columns:
    print("Error: Missing column 'woba_value' in the input file.")
    sys.exit(1)

# Calculate total bases as the sum of woba_value
total_bases = data['woba_value'].sum()

# Total number of batted ball events
total_batted_balls = len(data)

# Calculate SLG as total bases / total batted ball events
slg = total_bases / total_batted_balls

# Output the SLG
print(slg)
