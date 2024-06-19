import spotipy
from typing import List

from playlist import Playlist
from spotipy_auth import SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI, \
    SPOTIFY_CLIENT_SECRET
from track import Track


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
    def get_all_liked_songs(self) -> List[Track]:
        """
        NOTE: This function is time costly with large libraries.
        :return: large list of track objs
        """
        self._set_scope('user-library-read')
        results = self.sp.current_user_saved_tracks(limit=50)
        
        tracks_data = []
        while results['next']:
            tracks_data.extend(results['items'])
            results = self.sp.next(results)
            
            # DEBUG, avoids loading 5000+ songs in tests
            # if len(tracks_data) >= 200:
            #    break
            
        return [
            Track(
                t['track']['id'],
                t['track']['name'],
                ', '.join([i['name'] for i in t['track']['artists']]))
            for t in tracks_data
        ]

    def get_all_playlists(self) -> List[Playlist]:
        """
        :return: list of playlist objs
        """
        self._set_scope("playlist-read-private")
        results = self.sp.current_user_playlists()
        
        # Traverse paginated data
        playlist_data = results['items']
        while results['next']:
            results = self.sp.next(results)
            playlist_data.extend(results['items'])
        
        return [
            Playlist(p['id'], p['name'], p['description'], p['public'])
            for p in playlist_data
        ]
    
    def get_all_tracks_from_playlist(self, playlist_id: str) -> List[Track]:
        """
        :param playlist_id: playlist id
        :return: list of tracks in playlist, includes duplicates
        """
        self._set_scope("playlist-read-private")
        results = self.sp.playlist(playlist_id, fields="tracks,next")
        
        tracks_data = results['tracks']['items']
        results = results['tracks']
        while results['next']:
            results = self.sp.next(results)
            tracks_data.extend(results['items'])
        
        return [
            Track(
                t['track']['id'],
                t['track']['name'],
                ', '.join([i['name'] for i in t['track']['artists']]))
            for t in tracks_data
        ]
