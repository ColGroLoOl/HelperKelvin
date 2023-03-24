import os
from shutil import copyfile
from atexit import register as exitRegister
from datetime import datetime
from platform import system as getSystem


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

        self.logFile = open(f"{self.logFolder}\\latest.txt", "w+")
        self.logFile.flush()

    def postPrepLogs(self):
        """
        Organize the logs upon finish or crashed process
        :return:
        """
        now = datetime.now()
        time = now.strftime("%y-%m-%d_%H-%M-%S")

        self.logFile.close()

        copyfile(f"{self.logFolder}\\latest.txt", f"{self.logFolder}\\log-{time}.txt")

    def info(self, content: str) -> None:
        now = datetime.now()
        time = now.strftime("%d/%m %H:%M:%S.%f")

        print(
            bcolors.OKBLUE + time,
            bcolors.OKGREEN + f"[{self.name}\\{self.process}] [INFO]",
            bcolors.OKCYAN + content,
            bcolors.ENDC
        )

        self.logFile.write(f"{time} [{self.name}\\{self.process}] [INFO] {content}\n")

    def warn(self, content: str) -> None:
        now = datetime.now()

        print(
            bcolors.OKBLUE + now.strftime("%d/%m %H:%M:%S.%f"),
            bcolors.HEADER + f"[{self.name}\\{self.process}] [WARN]",
            bcolors.WARNING + content,
            bcolors.ENDC
        )

    def fail(self, content: str, exit: bool = True) -> None:
        now = datetime.now()

        print(
            bcolors.FAIL + bcolors.BOLD + now.strftime("%d/%m %H:%M:%S.%f"),
            bcolors.FAIL + f"[{self.name}\\{self.process}] [WARN]",
            bcolors.ENDC + bcolors.FAIL + content + ", exiting" if exit else ", ignored",
            bcolors.ENDC
        )
