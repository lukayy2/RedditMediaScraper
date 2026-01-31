class FileName:

    @staticmethod
    def splitFileExtension(strFileName: str) -> tuple[str, str]:
        """
        Splits the file name into name and extension.
        """

        intLastDotIndex = strFileName.rfind('.')
        if intLastDotIndex == -1:
            return strFileName, ''

        # if the extension is longer than 5 characters, we assume that it's not a valid extension
        if len(strFileName) - intLastDotIndex > 5:
            return strFileName, ''

        strName = strFileName[:intLastDotIndex]
        strExtension = strFileName[intLastDotIndex + 1:]
        return strName, strExtension
