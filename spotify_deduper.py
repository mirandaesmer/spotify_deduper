from typing import List, Tuple, Set

from constants import INCLUDE_GENRES, EXCLUDE_GENRES, IDEAL_PLAYLIST_LENGTH, \
    VALID_PLAYLIST_THRESHOLD
from genre import Genre
from playlist import Playlist
from spotipy_wrapper import SpotipyWrapper
from track import Track


class SpotifyDeduper:
    def __init__(self):
        self.wrapper = SpotipyWrapper()
        self.inc_genres = [
            Genre(g, include=True)
            for g in INCLUDE_GENRES
        ]
        self.exc_genres = [
            Genre(g, include=False)
            for g in EXCLUDE_GENRES
        ]
    
    def get_badly_labeled_playlists(self) -> List[Tuple[Playlist, str]]:
        valid_genre_names = INCLUDE_GENRES + EXCLUDE_GENRES
        playlists = self.wrapper.get_all_playlists()
        malformed_playlists = []
        
        for pl in playlists:
            if not len(pl.name):
                malformed_playlists.append((pl, 'NO PLAYLIST NAME'))
                continue
                
            if not len(pl.description):
                malformed_playlists.append((pl, 'NO GENRE TAG '))
                continue
            
            name_tkn = pl.name.split(' ')
            description_tkn = pl.description.split(' ')
            
            if description_tkn[0] not in valid_genre_names:
                malformed_playlists.append((pl, 'BAD GENRE TAG'))
                continue
            
            # Only query those that have passed all other filters
            tracks = self.wrapper.get_all_tracks_from_playlist(pl.id)
            pl.add_tracks(tracks)
            
            if name_tkn[0].isupper() and pl.length != IDEAL_PLAYLIST_LENGTH:
                malformed_playlists.append((pl, 'BAD PLAYLIST NAME'))
                continue
            elif (name_tkn[0].islower() and
                  pl.length >= VALID_PLAYLIST_THRESHOLD):
                malformed_playlists.append((pl, 'BAD PLAYLIST NAME'))
                continue

        return malformed_playlists
    
    def find_duplicates_single_playlist(self, playlist_id: str) -> Set[Track]:
        pl_tracks = self.wrapper.get_all_tracks_from_playlist(playlist_id)
        
        visited_ids = set()
        duplicates = set()
        
        for track in pl_tracks:
            if track.id in visited_ids:
                duplicates.add(track)
            else:
                visited_ids.add(track.id)
        return duplicates
