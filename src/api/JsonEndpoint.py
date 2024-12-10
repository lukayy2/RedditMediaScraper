import requests

from src.StdOut import StdOut


class JsonEndpoint:
    def __requestUrl(self, strUrl: str) -> requests.Response:
        objHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}
        StdOut.print('JsonEndpoint', 'GET {0}'.format(strUrl))
        return requests.get(strUrl, headers=objHeader, timeout=60)

    def requestUser(self, strUser: str, intLimit: int, strAfterToken: str) -> dict:
        strUrl: str = 'https://www.reddit.com/user/{0}/submitted.json?limit={1}&t=all'.format(strUser, intLimit)

        if len(strAfterToken) > 0:
            strUrl += '&after={0}'.format(strAfterToken)

        return self.__requestUrl(strUrl).json()

    def requestSubreddit(self, strSubreddit: str, intLimit: int, strAfterToken: str) -> dict:
        strUrl: str = 'https://www.reddit.com/r/{0}/new.json?limit={1}&t=all'.format(strSubreddit, intLimit)

        if len(strAfterToken) > 0:
            strUrl += '&after={0}'.format(strAfterToken)

        return self.__requestUrl(strUrl).json()
