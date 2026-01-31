from src.StdOut import StdOut
from src.api.parser.PostCollectionParser import PostCollectionParser
from src.download.PostDownloadController import PostDownloadController
from src.enum.TypeEnum import TypeEnum
import os
import json


class DebugPostCollectionController:

    def processDebugJson(self, strFilePath: str, outDir: str, objPostCollectionType: TypeEnum) -> None:
        """
        - parses debug json file to post collection
        - downloads all media in the post collection
        :param objPostCollectionType:
        :param strFilePath:
        :return:
        """
        if not os.path.exists(strFilePath):
            raise FileNotFoundError(f"File not found: {strFilePath}")

        with open(strFilePath, 'r') as file:
            strJson = file.read()

        dictJsonDebugPosts = json.loads(strJson)

        objPostCollectionParser = PostCollectionParser(objPostCollectionType, dictJsonDebugPosts)
        objPostCollection = objPostCollectionParser.parse()

        StdOut.print('DebugPostCollectionController', 'found {0} posts in debug json'.format(len(objPostCollection.ListPosts)))

        objPostDownloadController = PostDownloadController(outDir, False)

        intProcessedPosts = 1
        for post in objPostCollection.ListPosts:
            if not post.IsLink:
                StdOut.print('DebugPostCollectionController', 'start Post {0} ({1}/{2})'.format(post.ID, intProcessedPosts, len(post.arrMedia)))
                objPostDownloadController.downloadPost(post)

            intProcessedPosts = intProcessedPosts + 1
