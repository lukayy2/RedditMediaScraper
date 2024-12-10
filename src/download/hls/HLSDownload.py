import os
import shutil
import subprocess

import m3u8
import requests
from m3u8 import M3U8, Media, Segment

from src.Const import Const
from src.StdOut import StdOut
from src.download.hls.HLSParser import HLSParser


class HLSDownload:
    """
    Chooses best Quality from Master-Playlist m3u8
    -> uses HLSParser to chooses the best quality
    -> downloads Video and Audio chunks
    -> combines
    """

    def __init__(self, strUrl: str, strDestPath: str):
        self.__strUrl = strUrl
        self.__strBaseUrl = strUrl[:strUrl.rfind('/')+1]
        self.__strDestPath = strDestPath
        self.__strPathTmpDir = self.__strDestPath + '_tmp' + os.path.sep  # tmp dir for Video convertion

        self.__strPathMasterPlaylist = self.__strPathTmpDir + 'HLSPlaylist.m3u8'
        self.__strPathVideoPlaylist = self.__strPathTmpDir + 'HLS_Video.m3u8'
        self.__strPathAudioPlaylist = self.__strPathTmpDir + 'HLS_Audio.m3u8'

        self.__strPathVideoFile = self.__strPathTmpDir + 'HLS_Video.ts'
        self.__strPathAudioFile = self.__strPathTmpDir + 'HLS_Audio.aac'

    def download(self) -> int:
        self.__createTmpDir(self.__strPathTmpDir)
        objMasterPlaylist = self.__downloadPlaylist(self.__strUrl, self.__strPathMasterPlaylist)

        objHLSParser = HLSParser(objMasterPlaylist)
        objChosenPlaylist = objHLSParser.chooseBestQuality()

        strVideoPlaylistUrl = self.__strBaseUrl + objChosenPlaylist.uri

        objVideoPlaylist = self.__downloadPlaylist(strVideoPlaylistUrl, self.__strPathVideoPlaylist)
        listVideoSegments = self.__downloadContentFromPlaylist(objVideoPlaylist)
        self.__combineSegmentsToFile(listVideoSegments, self.__strPathVideoFile)

        # is there an Audio Track?
        if objChosenPlaylist.media:
            objMedia: Media = objChosenPlaylist.media[0]
            strAudioPlaylistUrl = self.__strBaseUrl + objMedia.uri

            objAudioPlaylist = self.__downloadPlaylist(strAudioPlaylistUrl, self.__strPathAudioPlaylist)
            listAudioSegments = self.__downloadContentFromPlaylist(objAudioPlaylist)
            self.__combineSegmentsToFile(listAudioSegments, self.__strPathAudioFile)

        self.__combineFilesVideoAndAudio(self.__strPathVideoFile, self.__strPathAudioFile, self.__strDestPath)

        # clean up
        if os.path.isdir(self.__strPathTmpDir):
            shutil.rmtree(self.__strPathTmpDir)

        return os.path.getsize(self.__strDestPath)

    def __downloadPlaylist(self, strUrl: str, strFilePath: str) -> M3U8:
        """
        Downloads a Playlist (text data)
        :param strUrl:
        :param strFilePath:
        :return:
        """
        objHeader = {'User-Agent': Const.HTTP_USER_AGENT}

        with requests.get(strUrl, headers=objHeader, timeout=60) as objResponse:
            if objResponse.status_code == 200:
                with open(strFilePath, 'wb') as objFile:
                    objFile.write(objResponse.content)
            else:
                raise RuntimeError('error download Playlist {0}, error: {1}'.format(strUrl, objResponse.status_code))

        return m3u8.load(strFilePath)

    def __downloadSegment(self, strSegmentUrl: str, strFilePath: str, intStartByte: int, intEndByte: int) -> None:
        """
        Downloads a Segment (binary data)
        :param strSegmentUrl:
        :param strFilePath:
        :param intStartByte:
        :param intEndByte:
        :return:
        """
        objHeader = {'User-Agent': Const.HTTP_USER_AGENT}

        if intStartByte > 0 or intEndByte > 0:
            objHeader['Range'] = 'bytes={0}-{1}'.format(intStartByte, intEndByte)

        with requests.get(strSegmentUrl, headers=objHeader, timeout=60, stream=True) as objStream:
            if objStream.status_code == 200 or objStream.status_code == 206:
                with open(strFilePath, 'wb') as objFile:
                    shutil.copyfileobj(objStream.raw, objFile)
            else:
                raise RuntimeError(
                    'error download Playlist {0}, error: {1}'.format(strSegmentUrl, objStream.status_code))

    def __downloadContentFromPlaylist(self, objPlaylist: M3U8) -> list[str]:
        """
        Downloads all Segments from a Playlist
        WARNING: Reddit is not using Chunked files, instead they use a Byte-Range for chunking
        Just in case, we download chunked with Byterange (like the Frontend does)

        :param objPlaylist:
        :return:
        """
        intSegmentCount = 0

        listSegments: list[str] = []

        for objSegment in objPlaylist.segments:
            objSegment: Segment = objSegment

            # StdOut.print('HLSDownload', 'Download segment {0}'.format(intSegmentCount))

            strDestFileName = objSegment.uri[:objSegment.uri.find('.')]
            strDestFileNameExt = objSegment.uri[objSegment.uri.find('.')+1:]

            strSegmentUrl = self.__strBaseUrl + objSegment.uri
            strSegmentFilePath = self.__strPathTmpDir + strDestFileName + '_' + str(intSegmentCount) + '_' + strDestFileNameExt
            intStartByte = 0
            intEndByte = 0

            strByteRange: str = objSegment.byterange

            arrByteRangeSplit: list[str] = strByteRange.split('@')

            if len(arrByteRangeSplit) == 2:
                intStartByte = int(arrByteRangeSplit[1])
                intEndByte = intStartByte + int(arrByteRangeSplit[0])

            if len(strByteRange) > 0 and intStartByte == 0 and intEndByte == 0:
                raise RuntimeError('Byterange error on segment: {0} on video: {1}'.format(objSegment.uri, self.__strBaseUrl))

            self.__downloadSegment(strSegmentUrl, strSegmentFilePath, intStartByte, intEndByte)
            listSegments.append(strSegmentFilePath)
            intSegmentCount += 1

        return listSegments

    def __combineSegmentsToFile(self, listSegments: list[str], strDestPath: str):
        """
        Takes list of Segments and combines them to one file
        :param listSegments:
        :param strDestPath:
        :return:
        """
        objDestFile = open(strDestPath, 'wb')
        for strSegmentPath in listSegments:
            objSegmentFile = open(strSegmentPath, 'rb')

            objDestFile.write(objSegmentFile.read())

            objSegmentFile.close()

        objDestFile.close()

    def __combineFilesVideoAndAudio(self, strPathVideoFile: str, strPathAutoFile: str, strPathCombined: str) -> None:

        listFFmpegArgs : list[str] = []

        listFFmpegArgs.append('ffmpeg')
        listFFmpegArgs.append('-i')
        listFFmpegArgs.append(strPathVideoFile)

        if os.path.isfile(strPathAutoFile):
            listFFmpegArgs.append('-i')
            listFFmpegArgs.append(strPathAutoFile)

        listFFmpegArgs.append('-c:v')
        listFFmpegArgs.append('copy')
        listFFmpegArgs.append('-c:a')
        listFFmpegArgs.append('copy')
        listFFmpegArgs.append(strPathCombined)

        objCompletedProcess = subprocess.run(listFFmpegArgs, capture_output=True)

        if objCompletedProcess.returncode > 1:
            print(objCompletedProcess.stdout)
            print(objCompletedProcess.stderr)
            raise RuntimeError('FFMPEG error on video {0}'.format(strPathCombined))

    def __createTmpDir(self, strPathTmp: str):
        if os.path.isdir(strPathTmp):
            shutil.rmtree(strPathTmp)

        os.makedirs(self.__strPathTmpDir)
