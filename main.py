import re
from flask import Flask, jsonify
import sqlite3

con = sqlite3.connect('product_showtimes.db')
cur = con.cursor()
latest_shows = cur.execute('SELECT * FROM latest_shows').fetchall()
movies = []
for movie in latest_shows:
    movies.append({
        'id': movie[0],
        'title': movie[1],
        'year': movie[2]
    })
app = Flask(__name__)

@app.route('/latest-shows')
def index():
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True)