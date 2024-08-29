import time
import json
from flask import Flask, redirect, request, jsonify, session, url_for
from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '123456'

PLAYLIST_ID = '31tnlbcr7llaf5ebpna5egqqymyu'

CLIENT_ID = 'c4984cb51a35439b92fb26bb9868c9f3'
CLIENT_SECRET = 'aa92998e9b8745fa8e363fe9a3c962a6'
REDIRECT_URI = 'http://localhost:6052/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return 'Welcome to my Spotify app <a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope,
        'show_dialog': 'true'
    }
    
    auth_url = f'{AUTH_URL}?{urlencode(params)}'

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        return redirect('/playlists')
    
    return 'Something went wrong'

@app.route('/playlists')
def playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }
    
    response = requests.get(f'{API_BASE_URL}me/playlists', headers=headers)
    playlists = response.json()
    
    return jsonify(playlists)

@app.route('/refresh_token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': session['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()
    
    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
    
    return redirect('/playlists')

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 6052, debug=True)


