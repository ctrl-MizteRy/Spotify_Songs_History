from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOauthError
from spotipy.oauth2 import SpotifyOAuth

class SpotifyScript:
    def __init__(self, client_id: str, client_secret: str):
        self.__CLIENT_ID = client_id
        self.__CLIENT_SECRET = client_secret
        self.current_time = []
        self.current_song = ""
        self.SCOPE = "user-read-private user-read-currently-playing"
        self.REDIRECT_URI = "http://localhost:8080/callback"
        try:
            self.__sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                client_id=self.__CLIENT_ID,
                client_secret= self.__CLIENT_SECRET,
                redirect_uri=self.REDIRECT_URI,
                scope=self.SCOPE
                ))
        except SpotifyOauthError as e:
            print("Error detected")
            raise Exception("Incorrect credentials!") from e

    def get_user(self):
        user = self.__sp.current_user()['display_name']
        print(f"Begin session\nLog-in as {user}.")
        return user

    def get_current_song(self):
        currently_playing = self.__sp.currently_playing()
        if currently_playing and currently_playing.get('is_playing'):
            song_name = currently_playing['item']['name']
            artist_name = ", ".join(artist['name'] for artist in currently_playing['item']['artists'])
            song_duration = currently_playing['item']['duration_ms']
            return [song_name, artist_name, song_duration]
        else:
            return None
    def update_song(self):
        song = self.get_current_song()
        if song:
            name = song[0]
            if name != self.current_song:
                self.current_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p").split(" ")
                listening_date = self.current_time[0]
                time_of_date = self.current_time[1]
                am_pm = self.current_time[2]
                artist = song[1]
                duration_ms = song[2]
                self.current_song = name
                return [listening_date, name, artist, time_of_date, am_pm, duration_ms]
        return None