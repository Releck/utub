utub
====
A quick project to scrape the total video length for a YouTube channel.
Intended for channels where this is non-trivial at 50 videos per request.

Needs Python 3.6 and a [YouTube API key](https://developers.google.com/youtube/v3/getting-started)

1. Set `YOUTUBE_API_KEY` in your environment.

1. Run tests
```pytest```

2. Run `python main.py --youtube-username <YouTube channel>`

If it fails while running, just run it again. It'll pick up where it left off.