from unittest import TestCase

from spotipy_test_data import TEST_PLAYLIST_1
from spotipy_wrapper import SpotipyWrapper


class SpotipyWrapperTests(TestCase):
    def setUp(self):
        self._wrapper = SpotipyWrapper()
    
    def test_get_all_liked_songs(self):
        # DEBUG, see get_all_liked_songs()
        tracks = self._wrapper.get_all_liked_songs()
        self.assertTrue(tracks)
        
    def test_get_all_playlists(self):
        playlist_data = self._wrapper.get_all_playlists()
        self.assertTrue(playlist_data)
    
    def test_get_all_tracks_from_playlist(self):
        # NOTE Uses test playlist data:
        tp1 = TEST_PLAYLIST_1
        tracks = self._wrapper.get_all_tracks_from_playlist(tp1['id'])
        self.assertTrue(tracks)
        self.assertEqual(len(tracks), 4)
