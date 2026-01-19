# Script to extract data from pokedata.ovh
# https://www.pokedata.ovh

import pandas as pd
import sqlite3

import requests
import certifi
import json

url = "https://www.pokedata.ovh/standingsVGC/0000164/masters/0000164_Masters.json"

try:
    # Use certifi's certificate bundle
    response = requests.get(url, verify=certifi.where())
    response.raise_for_status()
    data = response.json()
    
    print(f"Successfully retrieved data for {len(data)} players.")
    print(f"Tournament Winner: {data[0]['name']}")

    # Create a clean DataFrame with flattened columns
    players_data = []

    for player in data:
        player_info = {
            'name': player['name'],
            'placing': player['placing'],
            'wins': player['record']['wins'],
            'losses': player['record']['losses'],
            'ties': player['record']['ties'],
            'win_rate': player['record']['wins'] / (player['record']['wins'] + player['record']['losses'] + player['record']['ties']),
            'drop': player['drop'],
            'resistance_self': player['resistances']['self'],
            'resistance_opp': player['resistances']['opp'],
            'resistance_oppopp': player['resistances']['oppopp'],
        
            # Team composition info
            'team_size': len(player['decklist']),
            'pokemon_list': ', '.join([p['name'] for p in player['decklist']]),
            'tera_types': ', '.join([p['teratype'] for p in player['decklist']]),
            'items': ', '.join([p['item'] for p in player['decklist']]),
        
            # Round statistics
            'total_rounds': len(player['rounds']),
            'wins_in_rounds': sum(1 for r in player['rounds'].values() if r['result'] == 'W'),
            'losses_in_rounds': sum(1 for r in player['rounds'].values() if r['result'] == 'L'),
            'byes': sum(1 for r in player['rounds'].values() if r['name'] == 'BYE')
        }
        players_data.append(player_info)

        # Create the DataFrame
    df_players = pd.DataFrame(players_data)

    # Sort by placing
    df_players = df_players.sort_values('placing').reset_index(drop=True)

    print(f"DataFrame shape: {df_players.shape}")
    print("\nFirst few rows:")
    print(df_players[['name', 'placing', 'wins', 'losses', 'win_rate', 'pokemon_list', 'team_size']].head(10))
    
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")