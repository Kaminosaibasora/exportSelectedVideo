from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout
from PyQt5.QtCore import  Qt

class ScrollLabel(QScrollArea):
 
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs) 

        content = QWidget(self)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        lay = QVBoxLayout(content)
        lay.addWidget(self.label)

        self.setWidget(content)
        self.setWidgetResizable(True)
 
    def setText(self, text):
        self.label.setText(text)
    
    def text(self):
        return self.label.text()