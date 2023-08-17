from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QMovie

class AnimationWidget(QLabel):
    def __init__(self, path, x = 200, y = 200) -> None:
        super().__init__()
        self.setFixedSize(x, y)
        self.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(path)
        self.setMovie(self.movie)
        rect = self.geometry()
        size = QSize(min(rect.width(), rect.height()), min(rect.width(), rect.height()))
        self.movie.setScaledSize(size)
        self.adjustSize()
        
        # self.startAnimation()
        # self.show()

    def startAnimation(self):
        self.movie.start()
        # self.run = True
        # self.show()
    
    def stopAnimation(self):
        self.movie.stop()
        # self.run = False
        # self.close()

