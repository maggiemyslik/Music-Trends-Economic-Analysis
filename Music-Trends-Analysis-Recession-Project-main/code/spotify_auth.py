import requests 
import os
from dotenv import load_dotenv 
import base64
load_dotenv()

def get_token():
    '''
    gets the token to access the spotify API
    '''
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET") 

    url = 'https://accounts.spotify.com/api/token'

    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {'Authorization': f'Basic {auth_base64}'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url, headers=headers, data=data)

    access_token = response.json().get('access_token')
    return access_token