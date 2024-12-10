import os
import time

from src.RedditUrl import RedditUrl
from src.StdOut import StdOut
from src.data.Post import Post
from src.download.Downloader import Downloader
from src.enum.MediaEnum import MediaEnum
from src.enum.TypeEnum import TypeEnum


class PostDownloadController:
    def __init__(self, strBasePath: str, boolRequestThrottling: bool):
        self.strBasePath = strBasePath
        self.boolRequestThrottling = boolRequestThrottling
        self.objDownloader = Downloader()

    def downloadPost(self, objPost: Post) -> bool:

        boolMediaFound = False

        if len(objPost.arrMedia) > 0:
            strPath = self.strBasePath + os.path.sep

            if objPost.Type == TypeEnum.SubReddit:
                strPath += 'r' + os.path.sep
            else:
                strPath += 'u' + os.path.sep

            strPath += objPost.PostCollectionName + os.path.sep

            if not os.path.isdir(strPath):
                os.makedirs(strPath)

            for objMedia in objPost.arrMedia:

                if objMedia.MediaType == MediaEnum.Image:
                    strMediaID = RedditUrl.imageUrlToImageID(objMedia.Url)
                elif objMedia.MediaType == MediaEnum.Video:
                    strMediaID = RedditUrl.videoUrlToVideoID(objMedia.Url)
                else:
                    raise RuntimeError('unhandled MediaType!')

                strMediaPath = strPath + objPost.ID + '_' + strMediaID

                if not os.path.isfile(strMediaPath):
                    StdOut.print('PostDownloadController', 'download {0}'.format(strMediaID), '')

                    if objMedia.MediaType == MediaEnum.Image:
                        intFileSize = self.objDownloader.download(objMedia.Url, strMediaPath)
                    elif objMedia.MediaType == MediaEnum.Video:
                        intFileSize = self.objDownloader.downloadVideo(objMedia.Url, strMediaPath)
                    else:
                        raise RuntimeError('unhandled MediaType!')

                    StdOut.update(f' ({intFileSize/1000/1000:.2f} MB)')

                    os.utime(strMediaPath, (objPost.CreatedAtUTC, objPost.CreatedAtUTC))

                    if self.boolRequestThrottling:
                        time.sleep(0.5)
                else:
                    StdOut.print('PostDownloadController', 'file {0} already downloaded'.format(strMediaID))
                    boolMediaFound = True

        return boolMediaFound