class FileName:

    @staticmethod
    def splitFileExtension(strFileName: str) -> tuple[str, str]:
        """
        Splits the file name into name and extension.
        """

        intLastDotIndex = strFileName.rfind('.')
        if intLastDotIndex == -1:
            return strFileName, ''
        strName = strFileName[:intLastDotIndex]
        strExtension = strFileName[intLastDotIndex + 1:]
        return strName, strExtension
