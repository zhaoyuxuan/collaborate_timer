#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request,redirect,url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, 
    close_room, rooms, disconnect
import random, os

async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

@app.route('/')
def index():
    #random generate a room number for each study room
    number = str(random.randrange(100000,1000000000000000))
    return redirect("/"+number, code=302)

@app.route('/<roomNumber>')
def rommnum(roomNumber):
    #direct user to repective room based on the roomnumebr
    session['room'] = roomNumber
    return render_template('timer.html', async_mode=socketio.async_mode)

@socketio.on("create_new", namespace = "/sync")
def new():
    #put the newly joint user into the respective room
    if 'room' in session:
        emit('timer_syn', {'room':session['room']}, room=session['room'])
        join_room(session['room'])

@socketio.on('synchronize', namespace='/sync')
def sychronize(message):
    #get the time from one user and synchronize that
    emit('start_timer', {'currenttime':message['currenttime'], 'session':message['session'], 'pause':message["pause"], 'online':message["online"]}, room=message['room'])

@socketio.on('connect', namespace='/sync')
def connect():
    #when new user connect, sent a message to the javascript
    emit('new_connection', {'event':"new coming", "room":session["room"]}, room=session["room"])

@socketio.on('disconnect', namespace='/sync')
def disconnect():
    #called when user disconnect from the room
    emit('disconnection', {'event':"disconnect", "room":session["room"]}, room=session["room"])


if __name__ == '__main__':
    socketio.run(app)
