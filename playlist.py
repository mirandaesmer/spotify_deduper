class Playlist:
    def __init__(self, _id: str, name: str, description: str):
        self.id = _id
        self.name = name
        self.description = description
        
    def __str__(self):
        return f'\nPLAYLIST: {self.name} DESCRIPTION: {self.description}'
