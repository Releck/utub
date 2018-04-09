from lib import get_vid_ids, get_upload_playlist_id


def test_upload_playlist_id():
    upload_playlist_id = get_upload_playlist_id('HISTORY')
    assert upload_playlist_id == 'UULawgobP2qKULrmXTyFzWSQ'
    upload_playlist_id2 = get_upload_playlist_id('NBCNews')
    assert upload_playlist_id2 == 'UUeY0bbntWzzVIaj2z3QigXg'


def test_get_vid_ids():
    upload_playlist_id = get_upload_playlist_id('HISTORY')
    vid_ids = get_vid_ids(upload_playlist_id)
    known_ids = ['Ma-cvw-nFxM', 'KpEKVr41iPw', 'HvK4spglXD0', 'uIqDlDxCVYY', 'HgLLGIKjGw8']
    for known_id in known_ids:
        assert known_id in vid_ids
