from imdb import Cinemagoer
import sqlite3

# create an instance of the Cinemagoer class
ia = Cinemagoer()
top = ia.get_popular100_movies()
movie_list = []
for movie in top[:25]:
    movie_id = movie.movieID
    title = movie.data['title']
    year = movie.data['year']
    movie_list.append((movie_id, title, year))

con = sqlite3.connect('product_showtimes.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS latest_shows (id Numeric Primary Key, title text, year integer)""")
cur.executemany("INSERT INTO latest_shows VALUES (?, ?, ?)", movie_list)
con.commit()
con.close()