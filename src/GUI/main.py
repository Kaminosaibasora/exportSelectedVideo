import sys
sys.path.append('./engine')
from selectedfactory import SelectedFactory
from PyQt5.QtWidgets import QApplication
from GUI import GUI

sf = SelectedFactory()

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)

fen = GUI(sf)
fen.show()

app.exec_()