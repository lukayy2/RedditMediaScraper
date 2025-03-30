from src.RedditUrl import RedditUrl

from src.data.Media import Media
from src.data.Post import Post
from src.data.PostCollection import PostCollection
from src.enum.MediaEnum import MediaEnum
from src.enum.TypeEnum import TypeEnum


class PostCollectionParser:
    """
    Parses the Subreddit JSON into Posts
    """

    def __init__(self, objPostCollectionType: TypeEnum, dictJsonSubreddit: dict):
        self.__objPostCollectionType = objPostCollectionType
        self.__dictJsonSubreddit = dictJsonSubreddit

    def parse(self) -> PostCollection:
        listPosts: list[Post] = []

        for objChild in self.__dictJsonSubreddit['data']['children']:
            listMedia: list[Media] = []

            boolIsVideo = 'post_hint' in objChild['data'] and (objChild['data']['post_hint'] == 'hosted:video' or objChild['data']['post_hint'] == 'rich:video')
            boolIsLink = 'post_hint' in objChild['data'] and objChild['data']['post_hint'] == 'link'
            boolIsSelf = 'post_hint' in objChild['data'] and objChild['data']['post_hint'] == 'self'  # a Text post with a Thumbnail?

            boolIsExternalVideo = boolIsVideo and 'domain' in objChild['data'] and objChild['data']['domain'] == 'vimeo.com' # external Videos -> can't be processed (no reddit rendered preview)

            if not boolIsExternalVideo:
                boolIsExternalVideo = ('post_hint' in objChild['data'] and objChild['data']['post_hint'] == 'video'
                                       and 'domain' in objChild['data'] and objChild['data']['domain'] == 'dropbox.com')

            boolIsPinned = 'pinned' in objChild['data'] and objChild['data']['pinned']

            # we can't process vimeo Videos
            if not boolIsExternalVideo:
                # native reddit video
                if boolIsVideo and 'domain' in objChild['data'] and objChild['data']['domain'] == 'v.redd.it':
                    if 'media' in objChild['data'] and 'reddit_video' in objChild['data']['media']:
                        listMedia = self.__parseRedditVideo(objChild['data']['media']['reddit_video'])
                else:
                    # native image or gif
                    if 'media_metadata' in objChild['data']:
                        listMedia = self.__parseMediaMetadata(objChild['data']['media_metadata'])
                    else:
                        if 'preview' in objChild['data'] and not boolIsSelf:
                            # use reddit preview Video when it is an embedded, external hosted Video/gif
                            if 'reddit_video_preview' in objChild['data']['preview']:
                                listMedia = self.__parseRedditVideo(objChild['data']['preview']['reddit_video_preview'])
                            else:
                                # fallback..
                                listMedia = self.__parsePreview(objChild['data']['preview'])

            strPostCollectionName = objChild['data']['subreddit']

            if self.__objPostCollectionType == TypeEnum.User:
                strPostCollectionName = objChild['data']['author']

            listPosts.append(
                Post(
                    self.__objPostCollectionType,
                    objChild['data']['id'],
                    strPostCollectionName,
                    objChild['data']['title'],
                    boolIsLink,
                    boolIsPinned,
                    int(objChild['data']['ups']),
                    int(objChild['data']['downs']),
                    int(objChild['data']['created_utc']),
                    listMedia
                )
            )

        return PostCollection(
            self.__dictJsonSubreddit['data']['after'],
            self.__dictJsonSubreddit['data']['before'],
            listPosts
        )

    def __parsePreview(self, objPreviewData: dict) -> list[Media]:
        """
        parses the Preview Array in a list of images
        :param objPreviewData:
        :return:
        """
        listMedia: list[Media] = []

        if 'images' in objPreviewData:
            for objImageJson in objPreviewData['images']:
                strUrl = objImageJson['source']['url']

                listMedia.append(Media(RedditUrl.previewToImageUrl(strUrl), MediaEnum.Image))
        return listMedia

    def __parseMediaMetadata(self, objMediaMetadata: dict) -> list[Media]:
        """
        parses the Media Metadata in a list of Images
        :param objMediaMetadata:
        :return:
        """
        listMedia: list[Media] = []

        for strImageKey in objMediaMetadata.keys():
            objImageJson = objMediaMetadata[strImageKey]

            if objImageJson['status'] == 'valid':
                if objImageJson['e'] == 'Image' or objImageJson['e'] == 'AnimatedImage':
                    if objImageJson['e'] == 'AnimatedImage':
                        strImageUrl = objImageJson['s']['gif']
                    else:
                        strImageUrl = objImageJson['s']['u']
                    listMedia.append(Media(RedditUrl.previewToImageUrl(strImageUrl), MediaEnum.Image))

        return listMedia

    def __parseRedditVideo(self, objRedditVideo: dict) -> list[Media]:
        """
        parses the "reddit_video" tag within the "media" tag to a Video Element
        :param objRedditVideo:
        :return:
        """
        strVideoUrl: str = objRedditVideo['hls_url']

        if strVideoUrl.find('?') > 0:
            strVideoUrl = strVideoUrl[:strVideoUrl.find('?')]

        listMedia: list[Media] = [Media(strVideoUrl, MediaEnum.Video)]

        return listMedia
