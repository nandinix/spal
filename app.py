import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/login")
def login():
    return "<p>Login page</p>"

@app.route("/redirectPage")
def redirectPage():
    return "<p>Redirect</p>"

@app.route("/dashboard")
def dashboard():
    return "<p>Dashboard</p>"

if __name__ == '__main__':
    app.run(debug=True)