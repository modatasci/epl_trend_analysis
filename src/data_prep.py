
"""
This script serves to import, clean and prepare dataset for analysis
"""

# import libraries

import kagglehub
from pathlib import Path
import os
import pandas as pd

def set_path():
    # Get parent of notebooks directory
    project_root = Path.cwd() # Adjust .parent calls based on depth

    # Set the path to the data folder in this project
    data_path = project_root / "data"

    return project_root, data_path

# download dataset from kaggle: https://www.kaggle.com/datasets/marcohuiii/english-premier-league-epl-match-data-2000-2025
def scrap_raw_dataset():
    
    # get filepath
    project_root, data_path = set_path()

    # Download latest version of the data
    kagglehub.dataset_download("marcohuiii/english-premier-league-epl-match-data-2000-2025", output_dir=file_path, force_download=True)

def import_dataset():

    # get filepath
    project_root, data_path = set_path()

    df = pd.read_csv(f"{data_path}/epl_final.csv")

    return df

def format_dataset(df:pd.DataFrame):
    # get the match points earned by the home and away team
    match_stats = df[['Season','MatchDate','HomeTeam','AwayTeam','FullTimeHomeGoals','FullTimeAwayGoals','FullTimeResult']]

    match_stats['HomeTeamPoints'] = match_stats.apply(lambda row: 3 if row['FullTimeResult'] == 'H' else 1 if row['FullTimeResult'] == 'D' else 0, axis = 1)
    match_stats['AwayTeamPoints'] = match_stats.apply(lambda row: 3 if row['FullTimeResult'] == 'A' else 1 if row['FullTimeResult'] == 'D' else 0, axis = 1)

    # import additional data to fill in missing data from orignal dataset

    # get filepath
    project_root, data_path = set_path()

    additional_df_2425 = pd.read_csv(f"{data_path}/missing_season_24_25.csv")

    # convert timestamp to date
    additional_df_2425['MatchDate'] = pd.to_datetime(additional_df_2425['strTimestamp']).dt.strftime('%Y-%m-%d')

    additional_df_2425 = additional_df_2425[['Season','HomeTeam','FullTimeHomeGoals','AwayTeam','FullTimeAwayGoals','MatchDate']]

    # merge original data with additional data

    match_stats_2425 = match_stats[match_stats['Season'] == '2024/25']

    # additional_df_2425

    match_stats_2425 = additional_df_2425.merge(match_stats_2425, on=['Season','HomeTeam','AwayTeam','FullTimeHomeGoals','FullTimeAwayGoals','MatchDate'],how='left')

    # filling in missing data
    mask = match_stats_2425['FullTimeResult'].isna()
    match_stats_2425.loc[mask, 'FullTimeResult'] = match_stats_2425[mask].apply(
        lambda row: 'H' if row['FullTimeHomeGoals'] > row['FullTimeAwayGoals'] 
        else 'A' if row['FullTimeHomeGoals'] < row['FullTimeAwayGoals'] 
        else 'D', axis=1
    )

    mask = match_stats_2425['HomeTeamPoints'].isna()
    match_stats_2425.loc[mask, 'HomeTeamPoints'] = match_stats_2425[mask].apply(
        lambda row: 3 if row['FullTimeResult'] == 'H'
        else 0 if row['FullTimeResult'] == 'A'
        else 1, axis=1
    )

    mask = match_stats_2425['AwayTeamPoints'].isna()
    match_stats_2425.loc[mask, 'AwayTeamPoints'] = match_stats_2425[mask].apply(
        lambda row: 3 if row['FullTimeResult'] == 'A'
        else 0 if row['FullTimeResult'] == 'H'
        else 1, axis=1
    )

    match_stats_2425_complete = match_stats_2425.copy()

    # update original dataset - all season

    match_stats_complete = match_stats.merge(match_stats_2425_complete, on=['Season','MatchDate','HomeTeam','AwayTeam','FullTimeHomeGoals','FullTimeAwayGoals','FullTimeResult','HomeTeamPoints','AwayTeamPoints'],how='outer')

    # filter season - remove '2000/01', '2001/02', '2002/03', '2003/04', '2004/05'
    removed_season = ['2000/01', '2001/02', '2002/03', '2003/04', '2004/05']

    dataset = match_stats_complete[~match_stats_complete['Season'].isin(removed_season)]

    # get total points, points per game

    # get home team and away team points
    home_team_points = dataset.groupby(['Season','HomeTeam'])['HomeTeamPoints'].sum().reset_index()
    away_team_points = dataset.groupby(['Season','AwayTeam'])['AwayTeamPoints'].sum().reset_index()

    # aggregate points 
    total_points_by_season = home_team_points.merge(away_team_points,left_on=['Season','HomeTeam'], right_on=['Season','AwayTeam'])
    total_points_by_season['total_points'] = total_points_by_season['HomeTeamPoints'] + total_points_by_season['AwayTeamPoints']
    total_points_by_season['points_per_season'] = total_points_by_season['total_points'] / 38

    # get position rank
    total_points_by_season['rank'] = total_points_by_season.groupby('Season')['total_points'].rank(ascending=False, method='min').astype(int)

    return total_points_by_season

def main():
    print("This is the python script to prepare the data")


if __name__ == "__main__":
    main()