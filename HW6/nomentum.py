# Louis Romeo
# CSC 496 HW6
# nomentum.py


import os
import csv
import sys
from collections import defaultdict

def parse_arguments():
    # Parse command-line arguments
    if len(sys.argv) != 6:
        print("Usage: python nomentum.py <directory> <min_time> <yard_line> <max_score_diff> <start_transition>")
        sys.exit(1)

    directory = sys.argv[1]
    min_time = int(sys.argv[2])
    yard_line = int(sys.argv[3])
    max_score_diff = int(sys.argv[4])
    start_transition = int(sys.argv[5])  # 0 for turnover, 1 for punt, 2 for turnover on downs

    return directory, min_time, yard_line, max_score_diff, start_transition


def analyze_momentum(directory, min_time, yard_line, max_score_diff, start_transition):
    drive_results_count = defaultdict(int)
    total_drives = 0

    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            with open(file_path, mode="r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Check if the play starts a new drive
                    if row["play_id"] == row["drive_play_id_started"]:
                        # Apply filtering conditions
                        if (
                                int(row["half_seconds_remaining"]) >= min_time and
                                int(row["yardline_100"]) >= yard_line and
                                abs(int(row["score_differential"])) <= max_score_diff and
                                row["drive_start_transition"] == {0: "Turnover", 1: "Punt", 2: "Turnover on downs"}[
                            start_transition]
                        ):
                            # Increment count for the result of this drive
                            drive_result = row["fixed_drive_result"]
                            drive_results_count[drive_result] += 1
                            total_drives += 1

    # Print the results
    for result in sorted(drive_results_count.keys()):
        count = drive_results_count[result]
        percentage = (count / total_drives) * 100 if total_drives > 0 else 0
        print(f"{result}: {count} ({percentage:.2f}%)")

    print(f"Total: {total_drives}")


def main():
    directory, min_time, yard_line, max_score_diff, start_transition = parse_arguments()
    analyze_momentum(directory, min_time, yard_line, max_score_diff, start_transition)


if __name__ == "__main__":
    main()
