from unittest import TestCase

from spotify_deduper import SpotifyDeduper
from spotipy_test_data import TEST_PLAYLIST_1


class SpotifyDeduperTests(TestCase):
    def setUp(self):
        self.deduper = SpotifyDeduper()
        
    def test_get_badly_labeled_playlists(self):
        # Manually trigger 'NO GENRE TAG' ()
        # results = self.deduper.get_badly_labeled_playlists(debug=False)
        # bad_playlist = results[0][0].name
        # error_str = results[0][1]
        # self.assertEqual(bad_playlist, TEST_PLAYLIST_1['name'])
        # self.assertEqual(error_str, 'NO GENRE TAG')
        
        # Manually trigger 'BAD GENRE TAG'
        # results = self.deduper.get_badly_labeled_playlists(debug=True)
        # bad_playlist = results[0][0].name
        # error_str = results[0][1]
        # self.assertEqual(bad_playlist, TEST_PLAYLIST_1['name'])
        # self.assertEqual(error_str, 'BAD GENRE TAG')
        pass
        
    def test_find_duplicates_single_playlist(self):
        # contains a duplicate
        dupes = self.deduper.find_duplicates_single_playlist(
            TEST_PLAYLIST_1['id']
        )
        self.assertTrue(dupes)
        self.assertEqual(len(dupes), 1)
