from typing import List

from track import Track


class Playlist:
    def __init__(self, _id: str, name: str, description: str, public: bool):
        self.id = _id
        self.name = name
        self.description = description
        self.tracks = []
        self.length = 0  # how many songs in playlist
        self.public = public
        
    def add_tracks(self, tracks: List[Track]) -> None:
        self.tracks += tracks
        self.length = len(self.tracks)
