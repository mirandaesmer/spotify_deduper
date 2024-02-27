import spotipy
from typing import List, Tuple

from spotipy_auth import SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI, \
    SPOTIFY_CLIENT_SECRET


# TODO these are untested on latest version of Python/Spotipy
class SpotipyWrapper:
    def __init__(self):
        self.sp = None
    
    def _set_scope(self, scope: str) -> None:
        """
        Scopes Documentation:
        https://developer.spotify.com/documentation/general/guides/authorization/scopes/
        :param scope: Spotify permission str
        """
        self.sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope
        ))
    
    ###########################################################################
    # Spotipy API calls
    ###########################################################################
    def get_all_liked_songs(self) -> List[Tuple[str, str]]:
        # TODO api returns paged results
        return []
    
    def get_all_playlists(self) -> List[Tuple[str, str, str]]:
        """
        :return: list of playlists [('id', 'playlist_name', 'playlist_description')]
        """
        self._set_scope("playlist-read-private")
        results = self.sp.current_user_playlists()
        
        # Traverse paginated data
        playlist_data = results['items']
        while results['next']:
            results = self.sp.next(results)
            playlist_data.extend(results['items'])
        
        playlists = []
        for p in playlist_data:
            # print((p['id'], p['name'], p['description']))  # DEBUG
            playlists.append((p['id'], p['name'], p['description']))
        return playlists
    
    def get_all_tracks_from_playlist(self, p_id: str) -> List[Tuple[str, str]]:
        """
        :param p_id: playlist id
        :return: list of tracks in playlist [('id', 'name - artist')]
        """
        self._set_scope("playlist-read-private")
        results = self.sp.playlist(p_id, fields="tracks,next")
        
        songs_data = results['tracks']['items']
        results = results['tracks']
        while results['next']:
            results = self.sp.next(results)
            songs_data.extend(results['items'])
        
        songs = []
        for s in songs_data:
            song_id = s['track']['id']
            song_name = s['track']['name']
            song_artists = ', '.join([i['name'] for i in s['track']['artists']])
            
            # print(song_id, f"{song_name} - {song_artists}")  # DEBUG
            songs.append((song_id, f"{song_name} - {song_artists}"))
        return songs
