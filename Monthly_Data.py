import sqlite3
from datetime import datetime

class ReadData:
    def __init__(self):
        self.db = sqlite3.connect('Songs.db')
        self.cursor = self.db.cursor()
        month = datetime.today().month - 1 if datetime.today().month > 1 else 12
        self.month_str = str(month) if month >= 10 else "0" + str(month)
        self.month_str = self.month_str + "/%"

    def get_monthly_songs(self):
        self.cursor.execute("SELECT name FROM songs WHERE date LIKE ?", (self.month_str,))
        songs = {}
        names = self.cursor.fetchall()
        for name in names:
            if name[0] in songs:
                songs[name[0]] += 1
            else:
                songs[name[0]] = 1
        most_played_songs = dict(sorted(songs.items(), key=lambda x: x[1], reverse=True))
        return most_played_songs

    def get_play_time(self):
        time_spent = {}
        self.cursor.execute("SELECT date, time_ms FROM times WHERE date LIKE ?", (self.month_str,))        
        for date, time in self.cursor.fetchall():
            if date in time_spent:
                time_spent[date] += time
            else:
                time_spent[date] = time
        time_spent = dict(sorted(time_spent.items(), key=lambda x: x[1], reverse=True))
        return time_spent

    def get_total_time(self):
        data = self.get_play_time()
        times = list(data.values())
        total_time = 0
        for time in times:
            total_time += time
        return total_time

    def get_total_artist(self):
        self.cursor.execute("SELECT artist FROM songs WHERE date LIKE ?", (self.month_str,))
        artists = self.cursor.fetchall()
        most_played_artists = {}
        for artist in artists:
            names = artist[0].split(", ")
            for name in names:
                if name in most_played_artists:
                    most_played_artists[name] += 1
                else:
                    most_played_artists[name] = 1
        most_played_artists = dict(sorted(most_played_artists.items(), key=lambda x: x[1], reverse=True))
        return most_played_artists
