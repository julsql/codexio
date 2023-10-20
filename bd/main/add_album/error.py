from datetime import datetime
import os


class Error(Exception):

    def __init__(self, message_log, isbn=None, log_file_name="logs.txt"):
        __FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
        logfile = os.path.join(__FILEPATH__, "logs", log_file_name)
        self.addLog(logfile, message_log, isbn)
        print("Erreur : " + message_log)
        super().__init__(message_log)

    def addLog(self, logfile, message, isbn=None):
        f = open(logfile, "a", encoding="utf-8")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isbn is not None and isbn != "":
            f.write(f"\n{dt_string} {str(isbn)} : {message}")
        else:
            f.write(f"\n{dt_string} : {message}")
        f.close()
