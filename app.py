import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template
import time
from time import gmtime, strftime
import os

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
    if not token_info: 
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60 
    if (is_expired): 
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
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
    try: 
        token_info = get_token()
    except: 
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(
        auth=token_info['access_token'],
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

    if os.path.exists(".cache"): 
        os.remove(".cache")
    return render_template('dashboard.html', user_display_name = current_user_name, short_term_tracks=short_term_tracks, medium_term_tracks=medium_term_tracks, long_term_tracks=long_term_tracks, short_term_artists=short_term_artists, medium_term_artists=medium_term_artists, long_term_artists=long_term_artists, title = "Dashboard")


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return strftime("%a, %d %b %Y", date)

@app.template_filter('mmss')
def _jinja2_filter_miliseconds(time, fmt=None):
    time = int(time / 1000)
    minutes = time // 60 
    seconds = time % 60 
    if seconds < 10: 
        return str(minutes) + ":0" + str(seconds)
    return str(minutes) + ":" + str(seconds ) 


if __name__ == '__main__':
    app.run(debug=True)