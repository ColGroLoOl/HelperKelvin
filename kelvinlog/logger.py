import os
from shutil import copyfile
from atexit import register as exitRegister
from datetime import datetime
from platform import system as getSystem


class bColors:
    header = '\033[95m'
    okBlue = '\033[94m'
    okCyan = '\033[96m'
    okGreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


class getLogger:
    def __init__(self, name: str, process: str = "main", logFolder: str = "log"):
        self.name = name
        self.process = process

        self.logFile = None
        self.logFolder = logFolder
        self.prepLogs()

        # yea windows somehow fucks this up
        if getSystem() == "Windows":
            os.system("")

    def setProcess(self, new: str) -> None:
        self.process = new

    def prepLogs(self):
        """
            Check for the log folder and organize existing logs

        :return:
        """

        exitRegister(self.postPrepLogs)

        if not os.path.exists(self.logFolder):
            os.mkdir(self.logFolder)

        self.logFile = open(f"{self.logFolder}/latest.txt", "w+")
        self.logFile.flush()

    def postPrepLogs(self):
        """
            Organize the logs upon finish or crashed process

        :return:
        """
        now = datetime.now()
        time = now.strftime("%y-%m-%d_%H-%M-%S")

        self.logFile.close()

        copyfile(f"{self.logFolder}/latest.txt", f"{self.logFolder}/log-{time}.txt")

    def info(self, content: str) -> None:
        """
            Log given string in the console with fancy colors and save to a file

        :param content:
        :return:
        """
        now = datetime.now()
        time = now.strftime("%d/%m %H:%M:%S.%f")

        print(
            bColors.okBlue + time,
            bColors.okGreen + f"[{self.name}/{self.process}] [INFO]",
            bColors.okCyan + content,
            bColors.end
        )

        self.logFile.write(f"{time} [{self.name}/{self.process}] [INFO] {content}\n")

    def warn(self, content: str) -> None:
        """
            Same as info, but with different colors

        :param content:
        :return:
        """
        now = datetime.now()

        print(
            bColors.okBlue + now.strftime("%d/%m %H:%M:%S.%f"),
            bColors.header + f"[{self.name}/{self.process}] [WARN]",
            bColors.warning + content,
            bColors.end
        )

    def fail(self, content: str, exit: bool = True) -> None:
        """
            Same as warn, with the addition of the option to stop the running code

        :param content:
        :param exit:
        :return:
        """
        now = datetime.now()

        print(
            bColors.fail + bColors.bold + now.strftime("%d/%m %H:%M:%S.%f"),
            bColors.fail + f"[{self.name}/{self.process}] [WARN]",
            bColors.end + bColors.fail + content + ", exiting" if exit else ", ignored",
            bColors.end
        )
