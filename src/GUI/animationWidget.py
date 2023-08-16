from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QMovie

class AnimationWidget(QWidget):
    def __init__(self, path, x = 200, y = 200) -> None:
        super().__init__()
        self.run = False
        self.setFixedSize(x, y)
        self.label_animation = QLabel(self)
        self.label_animation.setMinimumSize(QSize(x, y))
        self.movie = QMovie(path)
        self.label_animation.setMovie(self.movie)
        # self.startAnimation()
        
        layout = QGridLayout()
        layout.addWidget(self.label_animation, 0, 0)
        self.setLayout(layout)
        # self.show()

    def startAnimation(self):
        self.movie.start()
        self.run = True
        self.show()
    
    def stopAnimation(self):
        self.movie.stop()
        self.run = False
        self.close()

