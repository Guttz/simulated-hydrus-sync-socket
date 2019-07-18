#!/usr/bin/env python
import uuid, json
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

# Modification table to hold modifications
modification_table = []


@app.route('/add-modification-table', methods=['GET', 'POST'])
def table_insert():
    new_row = request.get_json(force=True)
    new_job_id = str(uuid.uuid4())
    new_row['job_id'] = new_job_id
    modification_table.insert(0, new_row)
    socketio.emit('update',
                  {'last_job_id': new_job_id},
                  namespace='/sync')

    return str(new_job_id)


@app.route('/modification-table-diff')
def get_modification_table_diff():
    agent_job_id = request.args.get('agent_job_id')
    if not agent_job_id:
        return json.dumps(modification_table)

    for index, item in enumerate(modification_table):

        if item['job_id'] == agent_job_id:
            print("moddddddd table")
            print(modification_table[:index])
            return json.dumps(modification_table[:index])

    return json.dumps([])


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('broadcast_event', namespace='/sync')
def broadcast_message(message):
    emit('response',
         {'data': message['data']},
         broadcast=True)


@socketio.on('disconnect_request', namespace='/sync')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)


@socketio.on('connect', namespace='/sync')
def on_connect():
    pass


@socketio.on('disconnect', namespace='/sync')
def on_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
