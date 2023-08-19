import threading
from PyQt5.QtCore import QThread, pyqtSignal

class InfoThread(QThread):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

    def run(self, message):
        # print(threading.current_thread())
        print("INFO THREAD")
        info = self.gui.info.text()
        info += f"{message}\n"
        self.gui.info.setText(info)
        self.gui.info.update()
        self.finished.emit()
        
