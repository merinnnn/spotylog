class Track:
    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.artists = [artist["name"] for artist in data.get("artists", [])]
        self.album = data.get("album", {}).get("name")

    def __str__(self):
        return f"{self.name} by {', '.join(self.artists)}"

class Playlist:
    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.description = data.get("description")
        self.tracks = data.get("tracks", {}).get("items", [])

    def __str__(self):
        return f"{self.name} - {len(self.tracks)} tracks"