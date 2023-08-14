import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QAction, QFileDialog, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap
sys.path.append('./engine')
from selectedfactory import SelectedFactory

class GUI(QMainWindow):
    def __init__(self, sf, parent=None):
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Export Selected Video")
        self.sf = sf

        self.iconVideo          = QLabel()
        videoPixMap             = QPixmap("./GUI/static/videofile.png")
        self.iconVideo.setPixmap(videoPixMap)
        self.iconVideo.resize(videoPixMap.width()/2, videoPixMap.height()/2) # TODO : trouver une méthode qui fonctionne
        self.labelVideo         = QLabel("path video")
        self.pathButton         = QPushButton("Choose File")
        self.labelSoundTrack    = QLabel("Sound Track")
        self.selectedSoundTrack = QComboBox()
        self.labelSubTTrack     = QLabel("Subtitle Track")
        self.selectedSubTTrack  = QComboBox()
        self.generateVideo      = QPushButton("Generate")
        self.info               = QLabel("INFO")

        self.pathButton.clicked.connect(self.choosefilevideo)


        # LAYOUT
        layout = QGridLayout()
        layout.addWidget(self.iconVideo,            0, 0)
        layout.addWidget(self.labelVideo,           1, 0)
        layout.addWidget(self.pathButton,           2, 0)
        layout.addWidget(self.labelSoundTrack,      0, 1)
        layout.addWidget(self.selectedSoundTrack,   1, 1)
        layout.addWidget(self.labelSubTTrack,       0, 2)
        layout.addWidget(self.selectedSubTTrack,    1, 2)
        layout.addWidget(self.generateVideo,        1, 3)
        layout.addWidget(self.info,                 3, 0, 2, 4)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout)
        self.resize(1200, 720)

    def choosefilevideo(self):
        try :
            valid = False
            folderPath = ""
            while not valid :
                try :
                    folderPath = QFileDialog.getOpenFileUrl(self, "Choose Video File")
                    valid = True
                except Exception as e :
                    print(e)
            self.loadVideo(folderPath[0].path())
            
        except Exception as e :
            print(e)
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Error :"+str(e))
            error.setWindowTitle("Erreur de validation")
    
    def loadVideo(self, path):
        self.labelVideo.setText(path)
        self.sf.loadVideo(path)
        infoVideo = self.sf.info_video()
        print(infoVideo)
