import datetime


class StdOut:
    @staticmethod
    def print(strType: str, strMessage: str, strEnd='\n') -> None:
        objDateTimeNow = datetime.datetime.now()
        print('[{0}] [{1}]: {2}'.format(objDateTimeNow.strftime("%Y-%m-%d %H:%M:%S"), strType, strMessage), end=strEnd, flush=True)

    @staticmethod
    def update(strMessage: str) -> None:
        print(strMessage)
