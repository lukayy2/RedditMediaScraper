import time

from src.StdOut import StdOut
from src.api.JsonEndpoint import JsonEndpoint
from src.api.parser.PostCollectionParser import PostCollectionParser
from src.download.PostDownloadController import PostDownloadController
from src.enum.TypeEnum import TypeEnum


class PostCollectionDownloadController:
    """
    Download all Media from a User or Subreddit
    """

    def __init__(self):
        self.__intDownloadLimitApi = 100

    def download(self, objPostCollectionType: TypeEnum, strPostCollectionName: str, strOutDir: str, intPostLimit: int, boolRequestThrottling, boolDownloadAll: bool):

        intRemainingPosts: int = intPostLimit
        intDownloadedPosts: int = 0  # only for stat -> processed posts
        strAfterToken = ''

        objJsonAPI = JsonEndpoint()

        while intRemainingPosts > 0:
            StdOut.print('PostCollectionDownloadController', 'Remaining Posts to process: {0}'.format(intRemainingPosts))

            intCountPostsToRequest: int = self.__intDownloadLimitApi

            if intCountPostsToRequest > intRemainingPosts:
                intCountPostsToRequest = intRemainingPosts

            if objPostCollectionType == TypeEnum.SubReddit:
                dictJson = objJsonAPI.requestSubreddit(strPostCollectionName, intCountPostsToRequest, strAfterToken)
            else:
                dictJson = objJsonAPI.requestUser(strPostCollectionName, intCountPostsToRequest, strAfterToken)

            objPostCollectionParser = PostCollectionParser(objPostCollectionType, dictJson)
            objPostCollection = objPostCollectionParser.parse()

            objPostDownloadController = PostDownloadController(strOutDir, boolRequestThrottling)
            for objPost in objPostCollection.ListPosts:
                intDownloadedPosts += 1

                if not objPost.IsLink:
                    StdOut.print('PostCollectionDownloadController', 'start Post {0} ({1}/{2})'.format(objPost.ID, intDownloadedPosts, intPostLimit))
                    if objPostDownloadController.downloadPost(objPost):
                        # post is pinned, do not exit!
                        if objPost.IsPinned:
                            StdOut.print('PostCollectionDownloadController', 'Found pinned post already downloaded, skipping!')
                        elif not boolDownloadAll:
                            StdOut.print('PostCollectionDownloadController', 'Found already downloaded Media! reached end, exit!')
                            intRemainingPosts = 0
                            break
                    else:
                        time.sleep(2)

            strAfterToken = objPostCollection.AfterPointer
            intRemainingPosts -= self.__intDownloadLimitApi

            if strAfterToken is None:
                StdOut.print('PostCollectionDownloadController', 'reached end, no more Posts!')
                break
