# Music Library

[![CI](https://github.com/FuaadBashi/Music-Streaming-App/actions/workflows/ci.yml/badge.svg)](https://github.com/FuaadBashi/Music-Streaming-App/actions/workflows/ci.yml)

A console music-library service in Python. Build a song library, create free and premium
listeners, organise playlists, play and download songs, and get recommendations based on what a
playlist already contains.

```
'Road trip':
  - Bohemian Rhapsody by Queen (1 play)
You might also like:
  - Under Pressure by Queen
  - Imagine by John Lennon
```

## Highlights

- **Inheritance with real behavioural differences.** `FreeUser` hears an upgrade message before
  each song. `PremiumUser` can download. Both share `User`'s play-count and history logic.
- **Recommendations.** Suggests songs not yet in a playlist, ranking artists the playlist already
  features first and then the most-played songs.
- **Integrity rules.** Song and user IDs are unique, and a song can appear in a playlist only
  once. Violations raise a `MusicError` whose message the console shows.
- **Domain separate from I/O.** `music.py` uses dataclasses and has no `input()` or `print()`.
  `main.py` is the menu.

## Getting started

Requires Python 3.10+. No third-party packages are needed to run it.

```bash
git clone https://github.com/FuaadBashi/Music-Streaming-App.git
cd Music-Streaming-App
python3 main.py
```

Playback and downloads are simulated with console messages; data lives in memory for the session.

## Tests

```bash
pip install pytest ruff
pytest
ruff format --check . && ruff check .
```
