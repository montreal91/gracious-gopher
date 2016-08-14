
import time

from collections            import deque

from flask                  import Flask, render_template, session
from flask                  import jsonify, request
from flask.ext.bcrypt       import Bcrypt
from flask.ext.socketio     import SocketIO, emit, join_room
from flask.ext.socketio     import leave_room, close_room, rooms
from flask.ext.socketio     import disconnect
from flask.ext.sqlalchemy   import SQLAlchemy

from src.config             import BaseConfig

async_mode = None

app = Flask(__name__)
app.config.from_object(BaseConfig)

bcrypt      = Bcrypt(app)
db          = SQLAlchemy(app)
socketio    = SocketIO(app, async_mode=async_mode)

from src.models import GUser
thread = None

from src.snake import GSnake
from src.snake import DIRECTIONS
from src.point import GPoint

b = deque()
b.appendleft(GPoint(x=0, y=0))
b.appendleft(GPoint(y=1))
b.appendleft(GPoint(y=2))
snake           = GSnake(bodey=b)
tick            = 1
app.paused      = False
app.game_over   = False


def restart_game():
    b = deque()
    b.appendleft(GPoint(x=0, y=0))
    b.appendleft(GPoint(y=1))
    b.appendleft(GPoint(y=2))
    app.snake = GSnake(bodey=b)
    app.paused = False
    app.game_over = False


def background_thread():
    count = 0
    cols, rows = 8, 6
    x, y = 0,0
    restart_game()
    while True:
        socketio.sleep(tick)
        if not app.paused:
            app.snake.MakeStep()
        response = {}
        response["snake"] = app.snake.GetAsDict()
        response["game_over"] = not app.snake.is_alive
        response["apple"] = {"x":app.snake.apple.x, "y":app.snake.apple.y}
        response["field"] = {"width": cols, "height": rows}
        socketio.emit(
            "field_change",
            response,
            namespace="/test"
        )
        if not app.snake.is_alive:
            restart_game()
            socketio.sleep(2)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/register/", methods=["POST"])
def register():
    json_data = request.json
    user = GUser(
        email=json_data["email"],
        password=json_data["password"]
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = "success"
    except:
        status = "This user is already registered."
    db.session.close()
    return jsonify({"result": status})


@app.route("/api/login/", methods=["POST"])
def login():
    json_data = request.json
    user = GUser.query.filter_by(email=json_data["email"]).first()
    
    # TODO:  Wrap this complex condition into function
    if user and bcrypt.check_password_hash(
        user.password,
        json_data["password"]
    ):
        session["logged_in"] = True
        status = True
    else:
        status = False
    print(session["logged_in"])
    return jsonify({"result": status, "user": user.get_pk()})

@app.route("/api/logout/")
def logout():
    session.pop("logged_in", None)
    return jsonify({"result": "success"})

@app.route("/api/status/")
def status():
    if session.get("logged_in"):
        if session["logged_in"]:
            return jsonify({"status": True})
    else:
        return jsonify({"status": False})


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on("turn up", namespace="/test")
def turn_up(message):
    app.snake.ChangeDirection(DIRECTIONS.UP)


@socketio.on("turn right", namespace="/test")
def turn_right(message):
    app.snake.ChangeDirection(DIRECTIONS.RIGHT)


@socketio.on("turn left", namespace="/test")
def turn_left(message):
    app.snake.ChangeDirection(DIRECTIONS.LEFT)


@socketio.on("turn down", namespace="/test")
def turn_down(message):
    app.snake.ChangeDirection(DIRECTIONS.DOWN)


@socketio.on("toggle pause", namespace="/test")
def pause(message):
    print("poop")
    app.paused = not app.paused


@socketio.on("restart_game", namespace="/test")
def restart(message):
    restart_game()


@socketio.on('my ping', namespace='/test')
def ping_pong():
    emit('my pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
