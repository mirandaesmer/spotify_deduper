class Track:
    def __init__(self, _id: str, name: str, artist: str):
        self.id = _id
        self.name = name
        self.artist = artist
    
    def __str__(self):
        return f'\nTRACK: {self.name} ARTIST: {self.artist}'
