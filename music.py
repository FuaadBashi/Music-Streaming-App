"""Music library domain: songs, playlists, and free versus premium listeners."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


class MusicError(Exception):
    """A request that can't be carried out; the message is shown to the user."""


@dataclass
class Song:
    song_id: str
    title: str
    artist: str
    play_count: int = 0

    def __str__(self) -> str:
        plays = "1 play" if self.play_count == 1 else f"{self.play_count} plays"
        return f"{self.title} by {self.artist} ({plays})"


@dataclass
class User:
    user_id: str
    name: str
    history: list[Song] = field(default_factory=list)

    is_premium = False

    def play(self, song: Song) -> list[str]:
        """Plays a song and returns what the listener sees."""
        song.play_count += 1
        self.history.append(song)
        return [f"Now playing {song.title} by {song.artist}"]

    def download(self, song: Song) -> str:
        raise MusicError("Downloads are a premium feature. Upgrade to download songs.")


@dataclass
class FreeUser(User):
    def play(self, song: Song) -> list[str]:
        return ["Enjoy uninterrupted music by upgrading to premium!", *super().play(song)]


@dataclass
class PremiumUser(User):
    downloads: list[Song] = field(default_factory=list)

    is_premium = True

    def download(self, song: Song) -> str:
        if song in self.downloads:
            return f"{song.title} is already downloaded."
        self.downloads.append(song)
        return f"{song.title} by {song.artist} has been downloaded."


@dataclass
class Playlist:
    name: str
    songs: list[Song] = field(default_factory=list)

    def __str__(self) -> str:
        count = "1 song" if len(self.songs) == 1 else f"{len(self.songs)} songs"
        return f"{self.name} ({count})"

    def add(self, song: Song) -> None:
        if song in self.songs:
            raise MusicError(f"{song.title} is already in '{self.name}'.")
        self.songs.append(song)


class MusicService:
    def __init__(self):
        self.songs: dict[str, Song] = {}
        self.users: dict[str, User] = {}
        self.playlists: dict[str, Playlist] = {}

    def add_song(self, song_id: str, title: str, artist: str) -> Song:
        # Keyed by ID: the old check compared objects, so every new Song looked unique.
        if song_id in self.songs:
            raise MusicError(f"A song with ID {song_id} is already in the library.")
        song = Song(song_id, title, artist)
        self.songs[song_id] = song
        return song

    def add_user(self, user_id: str, name: str, premium: bool) -> User:
        if user_id in self.users:
            raise MusicError(f"User ID {user_id} is taken.")
        user = PremiumUser(user_id, name) if premium else FreeUser(user_id, name)
        self.users[user_id] = user
        return user

    def create_playlist(self, name: str) -> Playlist:
        if name in self.playlists:
            raise MusicError(f"A playlist named '{name}' already exists.")
        playlist = Playlist(name)
        self.playlists[name] = playlist
        return playlist

    def user(self, user_id: str) -> User:
        try:
            return self.users[user_id]
        except KeyError:
            raise MusicError(f"No user with ID {user_id}.") from None

    def playlist(self, name: str) -> Playlist:
        try:
            return self.playlists[name]
        except KeyError:
            raise MusicError(f"No playlist named '{name}'.") from None

    def recommend(self, playlist: Playlist, limit: int = 5) -> list[Song]:
        """Songs not yet in the playlist: artists it already features first, then most played."""
        artist_weight = Counter(song.artist for song in playlist.songs)
        candidates = [s for s in self.songs.values() if s not in playlist.songs]
        candidates.sort(key=lambda s: (-artist_weight[s.artist], -s.play_count, s.title))
        return candidates[:limit]
