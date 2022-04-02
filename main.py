from flask import Flask, jsonify,request,abort
import sqlite3

def connect(db):
    con = sqlite3.connect(db)
    return con
    

app = Flask(__name__)

@app.route('/movies')
def movies():
    con = connect('product_showtimes.db')
    cur = con.cursor()
    popular_movieset = cur.execute('SELECT * FROM movies').fetchall()
    con.close()
    movies = []
    for movie in popular_movieset:
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
        latest_showset = cur.execute('SELECT * FROM shows').fetchall()
        con.close()
        if len(latest_showset)==0:
            return jsonify({'response':'No Shows Found'})
        shows = []
        for show in latest_showset:
            shows.append({
            'id': show[0],
            'movie_id': show[1],
            'time': show[2],
            'price': show[3]
        })
        return jsonify(shows)
    elif request.method == 'POST':
        movie_id = request.json.get('movie_id')
        time_slot = request.json.get('time')
        price = request.json.get('price')
        query = f'Insert into shows (movie_id,time,price) values ({movie_id},\'{time_slot}\',{price});'
        try:
            cur.execute(query)
            con.commit()
            response = 'Successfully added new show'
        except Exception as e:

            response = 'Failed to add new show ' + str(e)
        finally:
            con.close()
            return {'response': response}  

@app.route('/users',methods=['GET', 'POST'])
def users():
    con = connect('product_showtimes.db')
    cur = con.cursor()
    if request.method == 'GET':
        userset = cur.execute('SELECT * FROM users').fetchall()
        con.close()
        if len(userset)==0:
            return jsonify({'response':'No Users Found'})
        users = []
        for user in userset:
            users.append({
            'id': user[0],
            'name': user[1],
            'phone': user[2],
            'email': user[3]
        })
        return jsonify(users)
    elif request.method == 'POST':
        name = request.json.get('name')
        phone = request.json.get('phone')
        email = request.json.get('email')
        query = f'Insert into users (name,phone,email) values (\'{name}\',\'{phone}\',\'{email}\');'
        try:
            cur.execute(query)
            con.commit()
            response = 'Successfully added a new user'
        except Exception as e:

            response = 'Failed to add new user ' + str(e)
        finally:
            con.close()
            return {'response': response}

@app.route('/booking',methods=['GET', 'POST'])
def book():
    con = connect('product_showtimes.db')
    cur = con.cursor()
    if request.method == 'GET':
        bookingset = cur.execute('SELECT * FROM tickets').fetchall()
        con.close()
        if len(bookingset)==0:
            return jsonify({'response':'No Seats Booked'})
        bookings = []
        for booking in bookingset:
            bookings.append({
            'id': booking[0],
            'show_id': booking[1],
            'seat_no': booking[2],
            'user_id': booking[3]
        })
        return jsonify(bookings)
    elif request.method == 'POST':
        show_id = request.json.get('show_id')
        seat_no = request.json.get('seat_no')
        user_id = request.json.get('user_id')
        query = f'Insert into tickets (show_id,seat_no,user_id) values (\'{show_id}\',\'{seat_no}\',\'{user_id}\');'
        try:
            cur.execute(query)
            con.commit()
            response = 'Successfully booked the ticket'
        except Exception as e:

            response = 'Failed to book ticket ' + str(e)
        finally:
            con.close()
            return {'response': response}   

@app.route('/booking/<ticket_id>',methods=['GET', 'PUT', 'DELETE'])
def booking(ticket_id):
    con = connect('product_showtimes.db')
    cur = con.cursor()
    if request.method == 'GET':
        query = f'Select * from tickets where id = {ticket_id}'
        ticket = cur.execute(query).fetchone()
        print(ticket)
        if ticket is None:
            abort(404)
        id = ticket[0]
        show_id = ticket[1]
        seat_no = ticket[2]
        user_id = ticket[3]
        return jsonify({'id': id, 'show_id': show_id, 'seat_no':seat_no, 'user_id':user_id})
    elif request.method == 'PUT':
        show_id = request.json.get('show_id')
        seat_no = request.json.get('seat_no')
        user_id = request.json.get('user_id')
        query = f'update tickets set show_id={show_id},seat_no={seat_no},user_id={user_id} where id={ticket_id}'
        try:
            cur.execute(query)
            con.commit()
            response = 'Successfully updated the ticket details'
        except Exception as e:

            response = 'Failed to update ticket ' + str(e)
        finally:
            con.close()
            return {'response': response}
    
    elif request.method == 'DELETE':
        query = f'delete from tickets where id={ticket_id}'
        try:
            cur.execute(query)
            con.commit()
            response = 'Successfully cancelled booking '
        except Exception as e:
            response = 'Failed to cancel booking ' + str(e)
        finally:
            con.close()
            return {'response': response}
            

     

if __name__ == '__main__':
    app.run(debug=True)