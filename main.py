from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv("PATH")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET= os.getenv("SPOTIPY_CLIENT_SECRET")
scope = "playlist-modify-private"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID, 
    client_secret=SPOTIPY_CLIENT_SECRET, 
    redirect_uri="https://example.com/", 
    scope=scope))

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")

soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.find_all(name="div", class_="o-chart-results-list-row-container")
titles = []
song_uri = []

user_id = spotify.current_user()["id"]

def get_track(track):
    try:
        results = spotify.search(q='track:' + track, type='track')
        song_uri.append(results['tracks']['items'][0]['uri'])
    except IndexError:
        print("couldn't find song")

def make_playlist():
    playlist = spotify.user_playlist_create(user=user_id,name=f"{user_date} Billboard 100", public=False)
    return playlist['id']

def add_tracks(songs):
    for song in songs:
        spotify.playlist_add_items(playlist_id=playlist_id,items=[song], position=None)

for song in songs:
    title = song.find(name="h3")
    title = title.get_text()
    str_title = title.replace('\n', '')
    str_title = str_title.replace('\t','')
    get_track(str_title)

playlist_id = make_playlist()
add_tracks(song_uri)
