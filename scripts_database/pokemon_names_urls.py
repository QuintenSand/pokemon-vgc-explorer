
import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import pandas as pd

# Fetch the webpage
url = "https://pokemondb.net/sprites"
response = requests.get(url)
response.raise_for_status()  # Check for HTTP errors

# Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Prepare lists for DataFrame
pokemon_ids = []
pokemon_names = []
image_urls = []

# Method 1: Look for infocard class (as you mentioned)
infocards = soup.find_all(class_="infocard")
for card in infocards:
    print(card)
    img_tags = card.find_all('img')
    for img in img_tags:
        if 'src' in img.attrs:
            image_urls.append(img['src'])

            # Get Pokémon name from alt text or nearby elements
            filename = img["src"].split('/')[-1]
            pokemon_name = filename.split('.')[0]
            pokemon_names.append(pokemon_name)

            # If ID not found, use sequential numbering
            pokemon_id = None
            if not pokemon_id:
                pokemon_id = len(pokemon_ids) + 1

            pokemon_ids.append(pokemon_id)

# Remove duplicates and display results
unique_urls = list(set(image_urls))
print(f"Found {len(unique_urls)} unique Pokémon image URLs")

# Print first 10 URLs as examples
for i, img_url in enumerate(unique_urls[:10]):
    print(f"{i+1}. {img_url}")

# Create DataFrame
pokemon_df = pd.DataFrame({
    'id': pokemon_ids,
    'name': pokemon_names,
    'url': image_urls
})

# write to sqlite
conn = sqlite3.connect("sqlite/pokemon_names_urls.db")
pokemon_df.to_sql(name="pokemon_names_urls", con = conn)
