class RedditUrl:
    @staticmethod
    def previewToImageUrl(strPreviewUrl: str) -> str:
        strUrl = strPreviewUrl.replace('preview', 'i')

        if strUrl.find('?') > 0:
            strUrl = strUrl[:strUrl.find('?')]
        return strUrl

    @staticmethod
    def imageUrlToImageID(strImageUrl: str) -> str:
        strImageUrl = strImageUrl[strImageUrl.find('redd.it/')+len('redd.it/'):]

        if strImageUrl.find('?') > 0:
            return strImageUrl[:strImageUrl.find('?')]

        return strImageUrl

    @staticmethod
    def videoUrlToVideoID(strVideoUrl: str) -> str:
        strVideoUrl = RedditUrl.imageUrlToImageID(strVideoUrl)
        return strVideoUrl[:strVideoUrl.find('/')] + '.mp4'
