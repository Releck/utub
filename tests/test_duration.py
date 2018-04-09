from lib import vid_length_from_id
from datetime import timedelta


def test_duration_from_vid_id():
    td = vid_length_from_id(vid_id='3p-Yqu0txIQ')
    assert td == timedelta(minutes=16, seconds=39)


def test_add_times_from_list():
    ids = ['3p-Yqu0txIQ', '1bQ4MwcVGdo', 'D3FoaYQQt4A']
    lengths = [vid_length_from_id(vid_id) for vid_id in ids]
    sum_length = sum(lengths, timedelta(0, 0))
    assert sum_length == timedelta(minutes=39, seconds=39)


def test_time_no_seconds():
    td = vid_length_from_id(vid_id='GQkYbOlK250')
    assert td == timedelta(minutes=10)


def test_time_with_hour():
    td = vid_length_from_id('38vn3xuLIQ8')
    assert td == timedelta(hours=1, minutes=13, seconds=7)
