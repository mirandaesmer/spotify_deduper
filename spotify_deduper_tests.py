from unittest import TestCase

from spotify_deduper import SpotifyDeduper
from spotipy_test_data import TEST_PLAYLIST_1


class SpotifyDeduperTests(TestCase):
    def setUp(self):
        self.deduper = SpotifyDeduper()
        
    def test_find_duplicates_single_playlist(self):
        # contains a duplicate
        dupes = self.deduper.find_duplicates_single_playlist(
            TEST_PLAYLIST_1['id']
        )
        self.assertTrue(dupes)
        self.assertEqual(len(dupes), 1)
