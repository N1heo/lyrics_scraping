from lyricsgenius import Genius
import pandas as pd
import csv
from preProc import clean_line

GENIUS_API_TOKEN = 'wUlLXbY_BaiC9mzO3RXR2-MpXEdkxuVdfem2SyxRSKKdLiVihVzYjlqI3dBWs2IW'

genius = Genius(GENIUS_API_TOKEN, verbose=False, remove_section_headers=True, skip_non_songs=True,
                excluded_terms=["(Remix)", "(Live)"])

# Function to fetch and store lyrics in a CSV file
def get_lyrics(tags, file_path):
    data = []
    for tag in tags:
        page = 1
        while page:
            try:
                res = genius.tag(tag, page=page)
                if not res['hits']:
                    break
                for hit in res['hits']:
                    song_lyrics = genius.lyrics(song_url=hit['url'])
                    song_lyrics = clean_line(song_lyrics)
                    data.append({"genre": tag, "lyrics": song_lyrics})
                page = res['next_page']
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
    lyrics_df = pd.DataFrame(data)
    lyrics_df.to_csv(file_path, index=False, encoding='utf-8')

# Tags to search
tags = ['rock', 'hip-hop', 'indie', 'heavy-metal', 'dance']
# tags = ['pop']
get_lyrics(tags, "lyrics_genre.csv")
