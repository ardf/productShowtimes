from imdb import Cinemagoer
import sqlite3

# create an instance of the Cinemagoer class
ia = Cinemagoer()
top = ia.get_popular100_movies()
movie_list = []
for movie in top[:25]:
    id = movie.movieID
    title = movie.data['title']
    year = movie.data['year']
    movie_list.append((id, title, year))

con = sqlite3.connect('product_showtimes.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS movies (id Numeric Primary Key, title text, year integer)""")
cur.executemany("INSERT OR IGNORE INTO movies VALUES (?, ?, ?)", movie_list)
con.commit()
con.close()