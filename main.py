"""Console front end for the music library."""

from music import MusicError, MusicService, Playlist, Song

MENU = """
Music Streaming App
 1. Create a user
 2. Add a song to the library
 3. Create a playlist
 4. Add a song to a playlist
 5. Play a song from a playlist
 6. Download a song (premium)
 7. View a playlist and recommendations
 8. View a user's play history
 9. View all songs
10. View all users
 0. Exit
"""


def ask(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        raise MusicError("A value is required.")
    return value


def pick(items: list, prompt: str):
    """Shows a numbered list and returns the chosen item; a bad number raises MusicError."""
    if not items:
        raise MusicError("There is nothing to choose from yet.")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    choice = input(prompt).strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(items):
        raise MusicError(f"Please enter a number from 1 to {len(items)}.")
    return items[int(choice) - 1]


def pick_playlist(service: MusicService) -> Playlist:
    return pick(list(service.playlists.values()), "Playlist number: ")


def pick_song(songs: list[Song]) -> Song:
    return pick(songs, "Song number: ")


def main() -> None:
    service = MusicService()

    while True:
        try:
            choice = input(MENU + "Enter your choice: ").strip()
            match choice:
                case "1":
                    user_id, name = ask("User ID: "), ask("Name: ")
                    premium = input("Premium account? (y/n): ").strip().lower() in ("y", "yes")
                    user = service.add_user(user_id, name, premium)
                    kind = "premium" if user.is_premium else "free"
                    print(f"Created {kind} user {user.name}.")
                case "2":
                    song = service.add_song(ask("Song ID: "), ask("Title: "), ask("Artist: "))
                    print(f"Added {song.title} to the library.")
                case "3":
                    playlist = service.create_playlist(ask("Playlist name: "))
                    print(f"Created playlist '{playlist.name}'.")
                case "4":
                    playlist = pick_playlist(service)
                    song = pick_song(list(service.songs.values()))
                    playlist.add(song)
                    print(f"Added {song.title} to '{playlist.name}'.")
                case "5":
                    user = service.user(ask("Your user ID: "))
                    playlist = pick_playlist(service)
                    for line in user.play(pick_song(playlist.songs)):
                        print(line)
                case "6":
                    user = service.user(ask("Your user ID: "))
                    print(user.download(pick_song(list(service.songs.values()))))
                case "7":
                    playlist = pick_playlist(service)
                    print(f"'{playlist.name}':")
                    for song in playlist.songs or ["(empty)"]:
                        print(f"  - {song}")
                    recommended = service.recommend(playlist)
                    if recommended:
                        print("You might also like:")
                        for song in recommended:
                            print(f"  - {song.title} by {song.artist}")
                case "8":
                    user = service.user(ask("User ID: "))
                    print(f"Play history for {user.name}:")
                    if not user.history:
                        print("  (nothing played yet)")
                    for song in user.history:
                        print(f"  - {song.title} by {song.artist}")
                case "9":
                    for song in service.songs.values() or ["(library is empty)"]:
                        print(f"  - {song}")
                case "10":
                    for user in service.users.values():
                        kind = "premium" if user.is_premium else "free"
                        print(f"  - {user.user_id}: {user.name} ({kind})")
                case "0":
                    print("Goodbye!")
                    break
                case _:
                    print("Please choose an option from the menu.")
        except MusicError as e:
            print(e)
        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()
