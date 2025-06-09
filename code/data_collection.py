import requests  # type: ignore

def get_spotify_id(song, artist, token):
    '''
    searches for a song and arist(s) in the spotify api,
    returns track_id, release_date, artist_id
    '''
    query = f"{song} {artist}"
    headers = headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.spotify.com/v1/search"
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get('tracks', {}).get('items', [])
        if items:
            track_id = items[0]['id']
            release_date = items[0]['album']['release_date']
            artist_id = items[0]['artists'][0]['id']
            return track_id, release_date, artist_id
    return None, None, None

def get_artist_genres(artist_id, token):
    '''
    searches an artist_id in the spotify api,
    returns a list of genres associated with the artist(s)
    '''
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("genres", [])
    return []
