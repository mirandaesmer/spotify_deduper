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
        :param debug: use only test playlists
        :return: List of tuples of playlist objects and related error message
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
    
    def _find_duplicate_tracks(self, track_list: List[Track]) -> Set[Track]:
        visited_ids = set()
        duplicates = set()
        
        for track in track_list:
            if track.id in visited_ids:
                duplicates.add(track)
            else:
                visited_ids.add(track.id)
        return duplicates
    
    def find_duplicates_single_playlist(self, playlist_id: str) -> Set[Track]:
        """
        :param playlist_id: spotify playlist id string
        :return: tracks that exist in both playlists
        """
        pl_tracks = self.wrapper.get_all_tracks_from_playlist(playlist_id)
        return self._find_duplicate_tracks(pl_tracks)
        
    def find_duplicates_multiple_playlists(
            self,
            playlist_ids: List[str],
    ) -> Set[Track]:
        """
        :param playlist_ids: spotify playlist id strings
        :return: tracks that exist in two or more playlists
        """
        all_tracks = []
        for pl_id in playlist_ids:
            all_tracks += self.wrapper.get_all_tracks_from_playlist(pl_id)
        return self._find_duplicate_tracks(all_tracks)

    def find_duplicates_in_genre(self, genre: str) -> Set[Track]:
        """
        :param genre: name of valid genre, defined in constants.py
        :return: tracks that exist in two or more playlists
        """
        playlists = self.wrapper.get_all_playlists()
        
        genre_playlist_ids = [
            pl.id for pl in playlists
            if pl.description and pl.description.split(' ')[0] != genre
        ]
        return self.find_duplicates_multiple_playlists(genre_playlist_ids)
    