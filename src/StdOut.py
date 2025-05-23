import datetime
import sys


class StdOut:
    @staticmethod
    def print(strType: str, strMessage: str, strEnd='\n') -> None:
        objDateTimeNow = datetime.datetime.now()
        print('[{0}] [{1}]: {2}'.format(objDateTimeNow.strftime("%Y-%m-%d %H:%M:%S"), strType, strMessage), end=strEnd, flush=True)

    @staticmethod
    def update(strMessage: str) -> None:
        print(strMessage)

    @staticmethod
    def err(strMessage: str) -> None:
        objDateTimeNow = datetime.datetime.now()
        print('\033[91m[{0}] [{1}]: {2}\033[0m'.format(objDateTimeNow.strftime("%Y-%m-%d %H:%M:%S"), 'error', strMessage), file=sys.stderr)