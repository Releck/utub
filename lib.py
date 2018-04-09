from collections import deque
from datetime import timedelta
import re
import requests
import os


REGEX_PATTERN = re.compile(r'PT(?P<hours>\d+H)?(?P<minutes>\d+M)?(?P<seconds>\d+S)?')


def get_upload_playlist_id(youtube_username):
    details_endpoint = 'https://www.googleapis.com/youtube/v3/channels'

    details_args = {
        'part': 'contentDetails',
        'forUsername': youtube_username,
        'key': os.environ['YOUTUBE_API_KEY']
    }

    res = requests.get(details_endpoint, params=details_args)
    upload_playlist_id = res.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return upload_playlist_id


def vid_length_from_id(vid_id):
    vids_endpoint = 'https://www.googleapis.com/youtube/v3/videos'

    vids_params = {
        'part': 'contentDetails',
        'key': os.environ['YOUTUBE_API_KEY'],
        'id': vid_id
    }

    res = requests.get(vids_endpoint, params=vids_params).json()
    duration = res['items'][0]['contentDetails']['duration']
    objs = re.match(REGEX_PATTERN, duration)
    matches = objs.groupdict('00')
    casted_matches = dict((k, int(v[:-1])) for k, v in matches.items())
    td = timedelta(**casted_matches)
    return td


def get_vid_ids(upload_playlist_id):
    playlist_args = {
        'part': 'contentDetails',
        'playlistId': upload_playlist_id,
        'key': os.environ['YOUTUBE_API_KEY'],
        'maxResults': 50,
    }

    vid_ids = deque()

    while True:
        playlists_endpoint = 'https://www.googleapis.com/youtube/v3/playlistItems'
        res = requests.get(playlists_endpoint, params=playlist_args)
        res_json = res.json()
        next_token = res_json.get('nextPageToken')

        for vid in res_json['items']:
            vid_ids.append(vid['contentDetails']['videoId'])
        if len(vid_ids) % 10000 == 0:
            print(f'{len(vid_ids)} found')
        if next_token is None:
            break
        else:
            playlist_args['pageToken'] = next_token
    return vid_ids
