# Reddit Subreddit/User Scraper

Downloading all Media from a Subreddit or User. Useful for getting lots of Pictures/Videos for AI stuff. <br/>
Paginates Subreddit/User Page with Posts ordered chronologically from newest to oldest.<br/>
Stops when a Media is found that is already downloaded!

---
## Requirements
 - Python >= 3.8
 - pip installed
---
## Basic Usage (Downloading Media from a Subreddit or User)
```
pip install -r requirements.txt
python3 main.py --outdir ./data/ --subreddit <NAME> --limit 1000
python3 main.py --outdir ./data/ --user <NAME> --limit 1000

python3 main.py --help # print help message
```

## Not stopping on already downloaded Media
```
python3 main.py --outdir ./data/ --subreddit <NAME> --limit 1000 --all
```

## Throttling requests 
```
python3 main.py --outdir ./data/ --subreddit <NAME> --limit 1000 --wait
```
---
## creation of venv
```
python3 -m venv ./.venv
source .venv/bin/activate
```
---