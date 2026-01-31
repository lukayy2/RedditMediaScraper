from src.CliInputParser import CliInputParser
from src.StdOut import StdOut
from src.SystemRequirements import SystemRequirements
from src.download.PostCollectionDownloadController import PostCollectionDownloadController
from src.enum.TypeEnum import TypeEnum
from src.download.DebugPostCollectionController import DebugPostCollectionController


class RedditScraper:
    def start(self) -> None:

        objSystemRequirements = SystemRequirements()
        objSystemRequirements.checkRequirements()

        objCliInputParser = CliInputParser()
        objConfig = objCliInputParser.parse()

        if objConfig.user is None and objConfig.subreddit is None:
            raise RuntimeError('No --user or --subreddit provided')

        if objConfig.subreddit is not None:
            StdOut.print('RedditScraper', 'Start Scraping Subreddit {0} for max {1} posts'.format(objConfig.subreddit, objConfig.limit))
            objPostCollectionType = TypeEnum.SubReddit
            strPostCollectionName = objConfig.subreddit
        else:
            StdOut.print('RedditScraper', 'Start Scraping User {0} for max {1} posts'.format(objConfig.user, objConfig.limit))
            objPostCollectionType = TypeEnum.User
            strPostCollectionName = objConfig.user

        if objConfig.wait:
            StdOut.print('RedditScraper', 'Throttling requests!')

        if objConfig.all:
            StdOut.print('RedditScraper', 'Running in "Download all" mode, not stopping on already downloaded Media')
        else:
            objConfig.all = False

        if objConfig.debugFile is not None:
            StdOut.print('RedditScraper', 'Debug file detected, no API calls!')

            try:
                objDebugPostCollectionController = DebugPostCollectionController()
                objDebugPostCollectionController.processDebugJson(objConfig.debugFile, objConfig.outdir,  objPostCollectionType)
            except Exception as e:
                StdOut.err(e.__str__())
                return

        else:

            objPostCollectionDownloadController = PostCollectionDownloadController()
            try:
                objPostCollectionDownloadController.download(objPostCollectionType, strPostCollectionName, objConfig.outdir, objConfig.limit, objConfig.wait, objConfig.all)
            except Exception as e:
                StdOut.err(e.__str__())
