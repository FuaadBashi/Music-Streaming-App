# Music Library — Python Console Simulation

An object-oriented Python exercise modeling users, premium users, songs, playlists, and an administrator-managed music library. Playback and downloads are simulated with console messages.

## Run locally

Requires Python 3.10 or later for structural pattern matching. No third-party packages are needed.

```bash
git clone https://github.com/FuaadBashi/Music-Streaming-App.git
cd Music-Streaming-App
python3 musicStreaming.py
```

Create a user, add songs, build a playlist, and use the menu to inspect play history.

## Code to explore

[musicStreaming.py](musicStreaming.py) contains the domain classes and interactive menu. The project demonstrates inheritance, object composition, collection management, and state changes across user actions.

Data lives in memory for the current session. There is no audio streaming service, persistent database, or authentication backend.
