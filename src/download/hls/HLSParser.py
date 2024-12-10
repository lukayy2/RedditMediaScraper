from m3u8 import M3U8
from m3u8.model import StreamInfo, Media, Playlist
from src.data.struct.RatedPlaylist import RatedPlaylist


class HLSParser:
    """
    Parsing m3u8 Playlists and choosing the best Quality of Audio+Video Stream
    """
    def __init__(self, objM3u8: M3U8):
        self.__objM3u8 = objM3u8
        self.__listRatetPlaylists: list[RatedPlaylist] = []

    def chooseBestQuality(self) -> Playlist:
        self.__listRatetPlaylists.clear()
        self.__rateQuality()

        objChosenPlaylist = None
        intCombinedQualityBest = 0

        for objRatetPlaylist in self.__listRatetPlaylists:
            intCombinedQuality = objRatetPlaylist.intAudioQuality + objRatetPlaylist.intVideoQuality

            if intCombinedQuality > intCombinedQualityBest:
                intCombinedQualityBest = intCombinedQuality
                objChosenPlaylist = objRatetPlaylist.objPlaylist

        if objChosenPlaylist is None:
            raise RuntimeError("failed to choose Playlist to download!")

        return objChosenPlaylist

    def __rateQuality(self) -> None:
        for objPlaylist in self.__objM3u8.playlists:
            objStreamInfo: StreamInfo = objPlaylist.stream_info

            intHeight = objStreamInfo.resolution[0]
            intWidth = objStreamInfo.resolution[1]

            intVideoQuality = intHeight + intWidth
            intAudioQuality = 0

            # sometimes gifs are delivered as HLS-Videos
            if objPlaylist.media:
                objMedia: Media = objPlaylist.media[0]

                strMediaUri: str = objMedia.uri
                strMediaUri = strMediaUri.lower()
                strMediaUri = strMediaUri.replace('hls_audio_', '')
                intAudioQuality = int(strMediaUri.replace('.m3u8', ''))

            objRatedPlaylist = RatedPlaylist(intVideoQuality, intAudioQuality, objPlaylist)
            self.__listRatetPlaylists.append(objRatedPlaylist)
