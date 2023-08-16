import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QAction, QFileDialog, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap
sys.path.append('./engine')
from selectedfactory import SelectedFactory
from animationWidget import AnimationWidget
import shutil
import threading
import os

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
        self.generateVideo.clicked.connect(self.generateVideoFinal)

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

        self.loadingScreen = AnimationWidget("./GUI/static/loading.gif", 800, 600)

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
        self.loadingScreen.startAnimation()
        self.labelVideo.setText(path)
        if os.path.exists(self.sf.fileout + "temp"):
            shutil.rmtree(self.sf.fileout + "temp")
        os.mkdir(self.sf.fileout + "temp")
        shutil.copy(path[1:], self.sf.fileout + "temp")
        path = self.sf.fileout + "temp/" + path.split("/")[-1]
        self.sf.loadVideo(path)

        load = threading.Thread(target=self.threadLoad)
        load.start()
        while load.is_alive():
            pass
        self.loadingScreen.stopAnimation()

    def threadLoad(self):
        infoVideo = self.sf.info_video()
        print(infoVideo)
        itemST = []
        for i in infoVideo['audio'] :
            itemST += [f"{i[0]} - {i[1]}"]
        self.selectedSoundTrack.addItems(itemST)
        itemST = [""]
        for i in infoVideo['subtt'] :
            itemST += [f"{i[0]} - {i[1]}"]
        self.selectedSubTTrack.addItems(itemST)
        self.sf.export_video_track()
        self.sf.export_audio_track()
        self.sf.export_subtitles()
        return

    def generateVideoFinal(self):
        generate = threading.Thread(target=self.threadGenerate)
        generate.start()
        while generate.is_alive():
            pass
        self.messageValidation()

    def threadGenerate(self):
        snt = int(self.selectedSoundTrack.currentText().split(" - ")[0])
        sbt = self.selectedSubTTrack.currentText().split(" - ")[0]
        if sbt == "":
            sbt = None
        else :
            sbt = int(sbt)
        print(snt)
        print(sbt)
        self.sf.assembly_video_audio_subtitle(snt, sbt)
        print("suppression des fichiers de construction")
        shutil.rmtree(self.sf.fileout + "temp")
        self.selectedSoundTrack.clear()
        self.selectedSubTTrack.clear()
        self.labelVideo.setText("")
        return
    
    def messageValidation(self):
        msgBox = QMessageBox()
        msgBox.setText("Video générée avec succès")
        msgBox.setWindowTitle("SUCCESS")
        msgBox.exec()

    def loadingAnimation(self):
        # self.loadingScreen = AnimationWidget("./GUI/static/loading.gif", 800, 600)
        self.loadingScreen.startAnimation()
        # while self.isLoading :
        #     pass
        # self.loadingScreen.stopAnimation()
        return
