import time
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

CLIENT_ID = "INSERT-CLIENT-ID"
CLIENT_SECRET = "INSERT-CLIENT-SECRET"
REDIRECT_URI = "http://localhost:8080/callback"


SCOPE = "user-read-private user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

currentSong = ""
def get_current_user():
    user = sp.current_user()
    print(f"Log-in as: {user['display_name']}")

# Get the currently playing song
def get_current_song():
    currently_playing = sp.currently_playing()
    if currently_playing and currently_playing.get('is_playing'):
        song_name = currently_playing['item']['name']
        artist_name = ", ".join(artist['name'] for artist in currently_playing['item']['artists'])
        return [song_name, artist_name]
    else:
        return []

def update_song():
    global currentSong
    data = []
    while True:
        song = get_current_song()
        if song:
            try:
                name = song[0]
                if name != currentSong:
                    current_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S%p").split(" ")
                    date = current_time[0]
                    time_of_date = current_time[1]
                    artist = song[1]
                    data.append([date,name,artist,time_of_date])
                    currentSong = name
                    time.sleep(10)
            except KeyboardInterrupt:
                break
    update_to_list(data)

def update_to_list(data):
    with open('SongHistory.csv', 'a', newline='') as csvfile:
        dw = csv.writer(csvfile)
        dw.writerows(data)


def main():
    get_current_user()
    get_playback()
    update_song()

if __name__ == "__main__":
    main()
