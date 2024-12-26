import os
import csv
import sys
# Author: Louis Romeo
# Date: 10/2/2024
# Purpose: the second analysis—the runner on second or runners on first and second, zero outs.
# The input and output formats are same as for part one.

def analyze_bunts_second_base(directory):
    # Directory should contain all 2430 csv files provided.
    num_bunts_laid_down = 0
    num_unsuccessful_sacrifices = 0
    num_successful_sacrifices = 0
    num_bunts_everyone_safe = 0
    num_missed_bunts = 0

    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)

            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    play_description = row[7].lower()  # Adjust as needed

                    # Check for bunt plays with runner on 2nd or 1st and 2nd
                    if 'bunt' in play_description and (
                            'on second' in row[3].lower() or 'on first and second' in row[3].lower()):
                        num_bunts_laid_down += 1

                        if 'foul' in play_description or 'miss' in play_description:
                            num_missed_bunts += 1
                        elif 'out at third' in play_description or 'out at second' in play_description:
                            num_unsuccessful_sacrifices += 1
                        elif 'advances' in play_description and 'out at first' in play_description:
                            num_successful_sacrifices += 1
                        elif 'safe' in play_description and 'bunt' in play_description:
                            num_bunts_everyone_safe += 1

    # Calculate rates
    sacrifice_rate = num_successful_sacrifices / num_bunts_laid_down if num_bunts_laid_down else 0
    hit_rate = num_bunts_everyone_safe / num_bunts_laid_down if num_bunts_laid_down else 0
    failure_rate = num_missed_bunts / num_bunts_laid_down if num_bunts_laid_down else 0

    # Output the results as specified
    print(f"numBuntsLaidDown: {num_bunts_laid_down}")
    print(f"numUnsuccessfulSacrifices: {num_unsuccessful_sacrifices}")
    print(f"numSuccessfulSacrifices: {num_successful_sacrifices}")
    print(f"numBuntsEveryoneSafe: {num_bunts_everyone_safe}")
    print(f"numMissedBunts: {num_missed_bunts}")
    print(f"sacrificeRate: {sacrifice_rate:.2f}")
    print(f"hitRate: {hit_rate:.2f}")
    print(f"failureRate: {failure_rate:.2f}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python hw3-bunt2.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    analyze_bunts_second_base(directory)
