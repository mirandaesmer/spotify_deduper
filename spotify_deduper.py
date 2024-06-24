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
    
    def get_badly_labeled_playlists(
            self,
            debug=False
    ) -> List[Tuple[Playlist, str]]:
        """
        :param debug: use only test playlists if true.
        :return: List of playlist objects in a tuple and labeling issue as str
        """
        valid_genre_names = INCLUDE_GENRES + EXCLUDE_GENRES
        playlists = self.wrapper.get_all_playlists()
        malformed_playlists = []
        
        if debug:
            playlists = list(filter(
                lambda p: 'TEST' in p.description, playlists
            ))
        
        for pl in playlists:
            if not len(pl.description):
                malformed_playlists.append((pl, 'NO GENRE TAG '))
                continue
            
            description_tkn = pl.description.split(' ')
            if description_tkn[0] not in valid_genre_names:
                malformed_playlists.append((pl, 'BAD GENRE TAG'))
                continue
            
            # Only query relevant playlists
            if not debug and description_tkn[0] not in INCLUDE_GENRES:
                continue

            tracks = self.wrapper.get_all_tracks_from_playlist(pl.id)
            pl.add_tracks(tracks)
            
            # NOTE: Spotify does not allow playlists with empty names
            title = pl.name.split(' - ')[0]
            if pl.length > IDEAL_PLAYLIST_LENGTH:
                malformed_playlists.append((pl, 'TOO MANY TRACKS'))
                continue
            elif title.isupper() and pl.length != IDEAL_PLAYLIST_LENGTH:
                malformed_playlists.append((pl, 'LENGTH NOT IDEAL'))
                continue
            elif title.islower() and pl.length >= VALID_PLAYLIST_THRESHOLD:
                malformed_playlists.append((pl, 'LENGTH ABOVE THRESHOLD'))
                continue
            elif (not title.islower() and not title.isupper()) \
                    and not (VALID_PLAYLIST_THRESHOLD < pl.length < IDEAL_PLAYLIST_LENGTH):
                malformed_playlists.append((pl, 'BAD PLAYLIST NAME'))
                continue
            # elif title.isupper() and not pl.public:
            #     malformed_playlists.append((pl, 'PUBLIC PLAYLIST IS PRIVATE'))
            #     continue
            # elif not (title.isupper()) and pl.public:
            #     malformed_playlists.append((pl, 'PRIVATE PLAYLIST IS PUBLIC'))
            #     continue
            
        return malformed_playlists
    
    def find_duplicates_single_playlist(self, playlist_id: str) -> Set[Track]:
        """
        :param: spotify playlist id string
        :return: set of track objs
        """
        pl_tracks = self.wrapper.get_all_tracks_from_playlist(playlist_id)
        
        visited_ids = set()
        duplicates = set()
        
        for track in pl_tracks:
            if track.id in visited_ids:
                duplicates.add(track)
            else:
                visited_ids.add(track.id)
        return duplicates
