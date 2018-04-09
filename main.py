from concurrent.futures import as_completed, ThreadPoolExecutor as Pool
from datetime import timedelta
from lib import vid_length_from_id, get_vid_ids, get_upload_playlist_id
import argparse
import os
import pickle
import logging
import sys


def vid_length_threads(vid_ids):
    with Pool(max_workers=100) as pool:
        for vid_id in vid_ids:
            future = pool.submit(vid_length_from_id, vid_id)
            yield future


def dump_ids(vid_ids):
    with open('vid_ids.txt', 'wb') as f:
        pickle.dump(vid_ids, f)


def load_ids():
    with open('vid_ids.txt', 'rb') as f:
        return pickle.load(f)


def persist_length_progress(results, i):
    with open(f'results/{i}.txt', 'wb') as f:
        return pickle.dump(results, f)


def get_latest_progress():
    os.makedirs('results', exist_ok=True)
    for root, dirs, files in os.walk('results'):
        largest = 0
        for file in files:
            i_file = int(file[:-4])
            if i_file > largest:
                largest = i_file
        return largest


def load_all_results():
    for root, dirs, files in os.walk('results'):
        return [pickle.load(open(f'{root}/{f}', 'rb')) for f in files]


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('--youtube-username', type=str, help='Name of youtube username to fetch')
    args = parser.parse_args()
    youtube_username = args.youtube_username
    upload_playlist_id = get_upload_playlist_id(youtube_username)

    try:
        vid_ids = load_ids()
    except:
        vid_ids = get_vid_ids(upload_playlist_id)
        dump_ids(vid_ids)

    largest = get_latest_progress()
    logging.info(f'Starting from {largest}')
    vid_ids = list(vid_ids)
    chunks = [vid_ids[i:i + 1000] for i in range(0, len(vid_ids), 1000)]
    for i, chunk in enumerate(chunks[largest:], start=largest):
        logging.info(f'Beginning chunk {i} of {len(chunks)}')
        lengths_futures = [vid_length for vid_length in vid_length_threads(chunk)]
        lengths = [length.result() for length in as_completed(lengths_futures)]
        sum_length = sum(lengths, timedelta(0, 0))
        logging.info(f'Sum of chunk {i}: {sum_length}')
        persist_length_progress(sum_length, i)

    logging.info('Finished all chunks, summing final')
    results = load_all_results()
    sum_total_length = sum(results, timedelta(0, 0))
    logging.info(f'Sum total length: {sum_total_length}')

if __name__ == '__main__':
    main()
