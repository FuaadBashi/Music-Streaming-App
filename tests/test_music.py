import pytest

from music import MusicError, MusicService


@pytest.fixture
def service():
    s = MusicService()
    s.add_song("s1", "Bohemian Rhapsody", "Queen")
    s.add_song("s2", "Don't Stop Me Now", "Queen")
    s.add_song("s3", "Imagine", "John Lennon")
    s.add_song("s4", "Under Pressure", "Queen")
    return s


def test_a_song_id_can_only_be_used_once(service):
    with pytest.raises(MusicError, match="already in the library"):
        service.add_song("s1", "Another Song", "Someone")


def test_a_user_id_can_only_be_used_once(service):
    service.add_user("u1", "Amina", premium=False)

    with pytest.raises(MusicError, match="taken"):
        service.add_user("u1", "Omar", premium=True)


def test_playing_counts_the_play_and_records_history(service):
    user = service.add_user("u1", "Amina", premium=True)
    song = service.songs["s3"]

    user.play(song)
    user.play(song)

    assert song.play_count == 2
    assert [s.title for s in user.history] == ["Imagine", "Imagine"]


def test_free_users_hear_an_upgrade_message_before_each_song(service):
    free = service.add_user("u1", "Amina", premium=False)

    lines = free.play(service.songs["s1"])

    assert lines[0].startswith("Enjoy uninterrupted music")
    assert lines[1] == "Now playing Bohemian Rhapsody by Queen"


def test_only_premium_users_can_download(service):
    free = service.add_user("u1", "Amina", premium=False)
    premium = service.add_user("u2", "Omar", premium=True)

    with pytest.raises(MusicError, match="premium feature"):
        free.download(service.songs["s1"])
    assert "downloaded" in premium.download(service.songs["s1"])
    assert premium.downloads == [service.songs["s1"]]


def test_a_song_appears_in_a_playlist_at_most_once(service):
    playlist = service.create_playlist("Road trip")
    playlist.add(service.songs["s1"])

    with pytest.raises(MusicError, match="already in 'Road trip'"):
        playlist.add(service.songs["s1"])


def test_recommendations_favour_artists_already_in_the_playlist(service):
    playlist = service.create_playlist("Queen favourites")
    playlist.add(service.songs["s1"])
    service.songs["s3"].play_count = 100  # popular, but a different artist

    recommended = [s.song_id for s in service.recommend(playlist)]

    assert recommended == ["s2", "s4", "s3"]


def test_unknown_users_and_playlists_are_reported(service):
    with pytest.raises(MusicError, match="No user with ID nobody"):
        service.user("nobody")
    with pytest.raises(MusicError, match="No playlist named 'Gym'"):
        service.playlist("Gym")
