
import time

from collections        import deque

from flask              import Flask, render_template, session
from flask              import request, redirect, url_for
from flask.ext.socketio import SocketIO, emit, join_room
from flask.ext.socketio import leave_room, close_room, rooms
from flask.ext.socketio import disconnect

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_login import logout_user, current_user

from oauth import OAuthSignIn

async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["OAUTH_CREDENTIALS"] = {
    "facebook": {
        "id": "650606668431442",
        "secret": "d9767807b88131d863160b4765575644"
    }
}
socketio = SocketIO(app, async_mode=async_mode)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = "index"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/authorize/<provider>/")
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route("/callback/<provider>/")
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash("Authentication failed.")
        return redirect(url_for("index"))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for("index"))

thread = None

from snake import GSnake
from snake import DIRECTIONS
from point import GPoint

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


if __name__ == "__main__":
    db.create_all()
    socketio.run(app, debug=True)
