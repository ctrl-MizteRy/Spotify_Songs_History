import sqlite3
from requests import ReadTimeout
from Spotify_Song import SpotifyScript
import time
from datetime import datetime
import schedule
from Send_Email import SendMail
from Monthly_Data import ReadData

db = sqlite3.connect('Songs.db')
cursor = db.cursor()
start_play = False
play_time_ms = 0
date_of_play = ""
def main():
    global start_play, play_time_ms, date_of_play
    try:
        sp_session = SpotifyScript('PUT-YOUR-CLIENT-ID HERE', 'PUT-YOUR-CLIENT-SECRET-HERE')
        user = sp_session.get_user()
    except Exception as e:
        print(f"Error detected: {e}")
        exit(1)
    create_db()
    while True:
        try:
            data = sp_session.update_song()
            is_playing = sp_session.get_current_song()
            if is_playing:
                if data:
                    if not start_play:
                        start_play = True
                        play_time_ms = datetime.now()
                        date_of_play = data[0]
                    date = data[0]
                    name = data[1]
                    artist = data[2]
                    time_of_date = data[3]
                    am_pm = data[4]
                    duration_ms = data[5]
                    cursor.execute('INSERT INTO songs (date, name, artist, time_of_date, duration_ms) VALUES (?, ?, ?, ?, ?)', (date, name, artist, (time_of_date+am_pm), duration_ms))
                    db.commit()
            else:
                if start_play:
                    start_play = False
                    time_spent = int((datetime.now() - play_time_ms).total_seconds() * 1000)
                    cursor.execute('INSERT INTO times (date, time_ms) VALUES (?,?)', (date_of_play, time_spent))
                    db.commit()
                    time.sleep(15)
                    if not is_playing:
                        sp_session.current_song = " "
                    continue
                time.sleep(10)
            if datetime.now().date() == 1:
                schedule.every().day.at("07:00").do(send_monthly_email())
        except KeyboardInterrupt:
            print(f"Ending session\nGood bye {user}.")
            break
        except ReadTimeout:
            time.sleep(20)
    cursor.close()
    db.close()

def create_db():
    global db, cursor
    if (cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='songs'").fetchone()) is None:
        cursor.execute('CREATE TABLE songs('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'date TEXT NOT NULL,'
                       'name TEXT NOT NULL,'
                       'artist TEXT NOT NULL,'
                       'time_of_date TEXT NOT NULL,'
                       'duration_ms INTEGER NOT NULL);')
        cursor.execute('CREATE TABLE times('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'date TEXT NOT NULL,'
                       'time_ms INTEGER NOT NULL);')
        db.commit()

def send_monthly_email():
    get_data = ReadData()
    gmail = SendMail()
    artists = get_data.get_total_artist()
    artists_name = list(artists.keys())
    artists_time_appear = list(artists.values())
    time_spent = get_data.get_total_time()
    songs = get_data.get_monthly_songs()
    songs_name = list(songs.keys())
    songs_time_appear = list(songs.values())
    with open('Monthly_Songs_Report.txt', 'w') as output:
        print("Monthly songs report from Spotify:", file=output)
        print(f"Total playing time of {datetime.now().month - 1} is {time_spent / 60000:.2f}m", file=output)
        print("Top 10 artists of the month:", file=output)
        for i in range(0,9):
            print(f"{i+1}- {artists_name[i]}, played a total of {artists_time_appear[i]} times.", file=output)
        print("Top 10 songs of the month:", file=output)
        for i in range(0,10):
            print(f"{i+1}- {songs_name[i]}, played a total of {songs_time_appear[i]} times", file=output)
        print("\n", file=output)
    gmail.sending_email()


if __name__ == '__main__':
    main()
