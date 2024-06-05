from typing import List

from playlist import Playlist


class Genre:
    def __init__(self, name: str, include: bool = True):
        self.name = name
        self.include = include
        self.playlists = []
        self.amount = 0  # how many playlists in this genre
    
    def add_playlists(self, playlists: List[Playlist]) -> None:
        self.playlists += playlists
        self.amount = len(self.playlists)
