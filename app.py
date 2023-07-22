import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'randomlongstringpasswordxydks'
TOKEN_INFO = 'token_info'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "ec719f6d9bd5467380200909ac20f409",
        client_secret= "ac50d2af91e44d6c920d954849e25c71",
        redirect_uri = url_for("redirectPage",_external=True),
        scope="user-top-read user-library-read"
    )

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    return token_info

@app.route("/")
def hello_world():
    return render_template('index.html', title='Welcome')

@app.route("/login")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirectPage")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info    
    return redirect(url_for("dashboard", _external=True))

@app.route("/dashboard")
def dashboard():
    user_token = get_token()
    sp = spotipy.Spotify(
        auth = user_token['access_token']
    )

    short_term_tracks = sp.current_user_top_tracks(
        limit = 10,
        offset = 0,
        time_range = "short_term"
    )
    medium_term_tracks = sp.current_user_top_tracks(
        limit = 10,
        offset = 0,
        time_range = "medium_term"
    )
    long_term_tracks = sp.current_user_top_tracks(
        limit = 10,
        offset = 0,
        time_range = "long_term"
    )

    short_term_artists = sp.current_user_top_artists(
        limit = 10,
        offset = 0,
        time_range = "short_term"
    )
    medium_term_artists = sp.current_user_top_artists(
        limit = 10,
        offset = 0,
        time_range = "medium_term"
    )
    long_term_artists = sp.current_user_top_artists(
        limit = 10,
        offset = 0,
        time_range = "long_term"
    )

    current_user_name = sp.current_user()['display_name']
    return render_template('dashboard.html', user_display_name = current_user_name, short_term=short_term_artists, medium_term=medium_term_artists, long_term=long_term_artists, title = "Dashboard")

if __name__ == '__main__':
    app.run(debug=True)