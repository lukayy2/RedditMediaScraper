import argparse


class CliInputParser:
    def parse(self):
        objParser = argparse.ArgumentParser()

        objParser.add_argument('--outdir', help='Output root path', required=True)
        objParser.add_argument('--subreddit', help='Subreddit to scrape')
        objParser.add_argument('--user', help='User to scrape')
        objParser.add_argument('--limit', help='Number of Posts to max scrape', default=100, type=int)
        objParser.add_argument('--wait', help='Flag to throttle Requests', action=argparse.BooleanOptionalAction, default=False)
        objParser.add_argument('--all', help='Flag to Scrape until limit. Instead of Scraping until last known Post', action=argparse.BooleanOptionalAction)

        return objParser.parse_args()