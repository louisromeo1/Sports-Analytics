import requests
from bs4 import BeautifulSoup, Comment
import time
import csv
import os

# Louis Romeo
# CSC 496 HW2
# Purpose: Program designed to scrape MLB play by play data from
#          baseball-reference.com for the 2023 MLB Season.

# File to track processed URLs
PROCESSED_URLS_FILE = 'processed_games.txt'

# Base URL for team schedules
BASE_URL = 'https://www.baseball-reference.com/teams/{}/2023-schedule-scores.shtml'

# Teams to scrape (you can add all MLB team abbreviations here)
teams = [
    'ARI',  # Arizona Diamondbacks
    'ATL',  # Atlanta Braves
    'BAL',  # Baltimore Orioles
    'BOS',  # Boston Red Sox
    'CHC',  # Chicago Cubs
    'CHW',  # Chicago White Sox
    'CIN',  # Cincinnati Reds
    'CLE',  # Cleveland Guardians
    'COL',  # Colorado Rockies
    'DET',  # Detroit Tigers
    'HOU',  # Houston Astros
    'KC',   # Kansas City Royals
    'LAA',  # Los Angeles Angels
    'LAD',  # Los Angeles Dodgers
    'MIA',  # Miami Marlins
    'MIL',  # Milwaukee Brewers
    'MIN',  # Minnesota Twins
    'NYM',  # New York Mets
    'NYY',  # New York Yankees
    'OAK',  # Oakland Athletics
    'PHI',  # Philadelphia Phillies
    'PIT',  # Pittsburgh Pirates
    'SD',   # San Diego Padres
    'SEA',  # Seattle Mariners
    'SF',   # San Francisco Giants
    'STL',  # St. Louis Cardinals
    'TB',   # Tampa Bay Rays
    'TEX',  # Texas Rangers
    'TOR',  # Toronto Blue Jays
    'WSH'   # Washington Nationals
]


# Delay between requests
DELAY_SECONDS = 5


def load_processed_urls():
    if not os.path.exists(PROCESSED_URLS_FILE):
        return set()
    with open(PROCESSED_URLS_FILE, 'r') as file:
        return set(line.strip() for line in file.readlines())


def save_processed_url(url):
    with open(PROCESSED_URLS_FILE, 'a') as file:
        file.write(url + '\n')


def process_game_page(game_url, team):
    # Check if already processed
    processed_urls = load_processed_urls()
    if game_url in processed_urls:
        print(f'Skipping already processed game: {game_url}')
        return

    response = requests.get(game_url)
    response.encoding = 'utf-8'  # Handle accented characters

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract comments in the HTML (this is where play-by-play data might be hidden)
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    # Parse and filter comments for the table of play-by-play data
    for comment in comments:
        if 'id="play_by_play"' in comment:
            play_by_play_soup = BeautifulSoup(comment, 'html.parser')
            rows = play_by_play_soup.find_all('tr')

            # Parse each row of play-by-play data
            for row in rows:
                cols = row.find_all('td')

                # Ensure there are at least 10 columns to avoid index error
                if len(cols) >= 10:
                    # Extract relevant data
                    inning = cols[0].text
                    score = cols[1].text
                    outs = cols[2].text
                    runners = cols[3].text
                    pitch_code = cols[4].text
                    win_prob_change = cols[5].text
                    current_win_prob = cols[6].text
                    play_description = cols[7].text
                    batter = cols[8].text
                    pitcher = cols[9].text

                    # Format the data into a CSV row
                    csv_row = [
                        inning, score, outs, runners, pitch_code, win_prob_change, current_win_prob, team, batter,
                        pitcher, play_description
                    ]

                    # Save to CSV
                    with open(f'./hw2_examples/{team}_games_2023.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_row)
                else:
                    print(f"Skipping row due to insufficient columns: {len(cols)} columns")

    # Mark game as processed
    save_processed_url(game_url)
    print(f'Processed game: {game_url}')


def scrape_team_schedule(team):
    url = BASE_URL.format(team)

    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all game links in the schedule
    game_links = soup.find_all('a', href=True)

    for link in game_links:
        game_url = link['href']
        if '/boxes/' in game_url:  # Game page link
            full_game_url = 'https://www.baseball-reference.com' + game_url
            process_game_page(full_game_url, team)
            time.sleep(DELAY_SECONDS)  # Delay to avoid getting blocked


def main():
    # Scrape all teams
    for team in teams:
        scrape_team_schedule(team)


if __name__ == '__main__':
    main()
