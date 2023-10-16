from datetime import datetime
import os


class Error:

    def __init__(self, message_log, isbn = None):
        __FILEPATH__ = os.path.dirname(os.path.abspath(__file__))
        self.log = os.path.join(__FILEPATH__, "logs.txt")
        self.addLog(message_log, isbn)
        print("___ERREUR___")
        print(message_log)

    def addLog(self, message, isbn = None):
        f = open(self.log, "a")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if isbn is not None:
            f.write("\n" + dt_string + " " + isbn + " : " + message)
        else:
            f.write("\n" + dt_string + " : " + message)
        f.close()
