#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request,redirect,url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import random,os




# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
app = Flask(__name__)
socketio = SocketIO(app, async_mode = async_mode)
thread = None
thread_lock = Lock()
app.config['SECRET_KEY']=os.environ['SECRET_KEY']


#random generate a room number for each study room
@app.route('/')
def index():
    maximum = 1000000000000000
    minimum = 100000
    number = str(random.randrange(minimum,maximum))
    return redirect("/"+number, code=302)


#direct user to repective room based on the roomnumebr
@app.route('/<roomnumber>')
def rommnum(roomnumber):
    session['room'] = roomnumber
    return render_template('timer.html', async_mode=socketio.async_mode)

#put the newly joint user into the respective room
@socketio.on("create_new",namespace = "/test")
def new():
    if 'room' in session:
        emit('timer_syn',{'room':session['room']},room = session['room'])
        join_room(session['room'])

#get the time from one user and synchronize that
@socketio.on('synchronize',namespace = '/test')
def sychronize(message):
    emit('start_timer',{'currenttime':message['currenttime'],'session':message['session'],'pause':message["pause"],'online':message["online"]},room = message['room'])
    print(message["pause"])

#when new user connect, sent a message to the javascript
@socketio.on('connect', namespace = '/test')
def connect():
    print('room'+session["room"])
    emit('new_connection',{'event':"new coming", "room":session["room"]},room = session["room"])

#called when user disconnect from the room
@socketio.on('disconnect', namespace = '/test')
def disconnect():
    print(session["room"])
    emit('disconnection', {'event':"disconnect","room":session["room"]},room = session["room"])


if __name__ == '__main__':
    socketio.run(app)
