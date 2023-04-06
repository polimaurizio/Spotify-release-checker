import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import os
from dotenv import load_dotenv

load_dotenv() 

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Autenticazione all'API di Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ID dell'artista di cui verificare se ha pubblicato un nuovo album o singolo
artist_id = os.getenv("ARTIST_ID")

# Recupero gli album e i singoli dell'artista
albums = sp.artist_albums(artist_id, album_type='album')
singles = sp.artist_albums(artist_id, album_type='single')
artist = sp.artist(artist_id)

# Controllo l'ultima data di pubblicazione dell'album o del singolo dell'artista
latest_release_date = None
for album in albums['items']:
    release_date_str = album['release_date']
    release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%d')
    if latest_release_date is None or latest_release_date < release_date:
        latest_release_date = release_date

for single in singles['items']:
    release_date_str = single['release_date']
    release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%d')
    if latest_release_date is None or latest_release_date < release_date:
        latest_release_date = release_date

# Verifico se l'ultimo album o singolo è stato pubblicato negli ultimi 30 giorni
if latest_release_date is not None:
    days_since_last_release = (datetime.datetime.now() - latest_release_date).days
    if days_since_last_release <= 30:
        print(f"L'artista: {artist['name']} ha pubblicato un nuovo album o singolo pochi giorni fa intitolato: {single['name']}.")
    else:
        print(f"L'artista: {artist['name']} non ha pubblicato nuovi album o singoli negli ultimi giorni.")
else:
    print(f"L'artista: {artist['name']} non ha album o singoli disponibili su Spotify.")
