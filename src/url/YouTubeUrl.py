import re


class YouTubeUrl:

    @staticmethod
    def videoUrlToVideoID(strVideoThumbnailUrl: str) -> str:
        """
        Extracts the YouTube video ID from a thumbnail url
        :param strVideoThumbnailUrl: The YouTube image URL
        :return: The video ID as a string, or None if not found
        """
        match = re.search(r"ytimg\.com/vi/([A-Za-z0-9._%-]{11})/", strVideoThumbnailUrl)
        if match:
            return match.group(1)

        raise RuntimeError('Unable to extract Youtube Video id from Thumbnail url {0}'.format(strVideoThumbnailUrl))
