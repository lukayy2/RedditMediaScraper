import os.path
import shutil

import requests

from src.Const import Const
from src.download.hls.HLSDownload import HLSDownload


class Downloader:

    def download(self, strUrl: str, strDestImage: str) -> int:
        objHeader = {'User-Agent': Const.HTTP_USER_AGENT}
        with requests.get(strUrl, headers=objHeader, timeout=60, stream=True) as objStream:
            with open(strDestImage, 'wb') as objFile:
                shutil.copyfileobj(objStream.raw, objFile)
                return os.path.getsize(strDestImage)

    def downloadVideo(self, strUrl: str, strDestPath: str) -> int:
        objHlsDownload = HLSDownload(strUrl, strDestPath)
        return objHlsDownload.download()
