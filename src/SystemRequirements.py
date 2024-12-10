import subprocess
import sys


class SystemRequirements:

    def checkRequirements(self) -> None:
        self.__checkPythonVersion()
        self.__checkSystemPackagesInstalled()

    def __checkPythonVersion(self) -> None:
        if sys.version_info < (3, 8):
            raise RuntimeError('Only tested with Python >= 3.8')

    def __checkSystemPackagesInstalled(self) -> None:
        objCompletedProcess = subprocess.run(['ffmpeg'], shell=True, capture_output=True)
        # 0 and 1 are ok
        if objCompletedProcess.returncode > 1:
            raise RuntimeError('ffmpeg not installed on System!')
