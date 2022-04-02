from flask import Flask, jsonify,request,json
import sqlite3

def connect(db):
    con = sqlite3.connect(db)
    return con
    

app = Flask(__name__)

@app.route('/movies')
def movies():
    con = connect('product_showtimes.db')
    cur = con.cursor()
    popular_movies = cur.execute('SELECT * FROM movies').fetchall()
    con.close()
    movies = []
    for movie in popular_movies:
        movies.append({
            'id': movie[0],
            'title': movie[1],
            'year': movie[2]
        })
    return jsonify(movies)

@app.route('/latest-shows',methods=['GET', 'POST'])
def latest_shows():
    con = connect('product_showtimes.db')
    cur = con.cursor()
    if request.method == 'GET':
        latest_shows = cur.execute('SELECT * FROM shows').fetchall()
        con.close()
        if len(latest_shows)==0:
            return jsonify({'response':'No Shows Found'})
        shows = []
        for show in latest_shows:
            shows.append({
            'id': show[0],
            'movie_id': show[1],
            'time': show[2],
            'price': show[3]
        })
        return jsonify(shows)
    elif request.method == 'POST':
        print("hello",request.json)
        id = request.json.get('id')
        movie_id = request.json.get('movie_id')
        time_slot = request.json.get('time_slot')
        price = request.json.get('price')
        query = f'Insert into shows values ({id},{movie_id},\'{time_slot}\',{price});'
        print(query)
        try:
            cur.execute(query)
            con.commit()
            response = 'Successfully added new show'
        except Exception as e:

            response = 'Failed to insert new show ' + str(e)
        finally:
            con.close()
            return {'response': response}        

if __name__ == '__main__':
    app.run(debug=True)