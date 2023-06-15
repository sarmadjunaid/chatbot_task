from flask import Flask, session, redirect, url_for, render_template
from authlib.integrations.flask_client import OAuth
from flask_socketio import SocketIO
from utils import login_required
from loguru import logger
from urllib.parse import quote_plus, urlencode
from config import DOMAIN, CLIENT_ID, CLIENT_SECRET
from auth import AuthManager

app = Flask(__name__)

socketio = SocketIO(app, async_mode='gevent', engineio_logger=True)
oauth = OAuth(app)

auth = AuthManager()

app.secret_key = 'your_secret_key'

authO = oauth.register('auth0',
                       client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       api_base_url=f'https://{DOMAIN}',
                       access_token_url=f'https://{DOMAIN}/oauth/token',
                       authorize_url=f'https://{DOMAIN}/authorize',
                       client_kwargs={
                           'scope': 'openid profile email',
                       },
                       server_metadata_url=f'https://{DOMAIN}/.well-known/openid-configuration')


@app.route('/')
@login_required
def index():
    return render_template('chat.html')


@socketio.on('connect')
def handle_connect():
    logger.success('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    logger.success('Client disconnected')


@socketio.on('message')
def handle_message(data):
    logger.info(f'Received message: {data}')
    socketio.emit('message', data)  # Echo the message back to the client


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token = oauth.auth0.authorize_access_token()
    auth.handle_user_data(userinfo=token.get('userinfo'), token=token.get('access_token'))
    session['userinfo'] = token.get('userinfo')
    return redirect("/")


@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("login", _external=True),
                "client_id": CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    socketio.run(app)
