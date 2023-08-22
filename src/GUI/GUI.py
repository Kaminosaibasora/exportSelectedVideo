import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox,  QFileDialog, QPushButton, QLabel, QComboBox, QProgressBar
from PyQt5.QtCore import  Qt, QThread, pyqtSignal as Signal, pyqtSlot as Slot, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from loadworker import LoadWorker
sys.path.append('./engine')
from selectedfactory import SelectedFactory
from scrollLabel import ScrollLabel
import shutil
import os
from generateworker import GenerateWorker
import subprocess

class GUI(QMainWindow):
    def __init__(self, sf, parent=None):
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Export Selected Video")
        self.sf = sf

        self.iconVideo          = QLabel()
        self.iconSound          = QLabel()
        self.iconSubtt          = QLabel()
        videoPixMap             = QPixmap("./GUI/static/videofile.png")     .scaled(100, 100)
        soundPixMap             = QPixmap("./GUI/static/soundtrack.png")    .scaled(100, 100)
        subttPixMap             = QPixmap("./GUI/static/subtitletrack.png") .scaled(100, 100)
        self.iconVideo.setPixmap(videoPixMap)
        self.iconSound.setPixmap(soundPixMap)
        self.iconSubtt.setPixmap(subttPixMap)

        self.labelVideo         = QLabel        ("path video")
        self.pathButton         = QPushButton   ("Choose File")
        self.labelSoundTrack    = QLabel        ("Sound Track")
        self.selectedSoundTrack = QComboBox     ()
        self.labelSubTTrack     = QLabel        ("Subtitle Track")
        self.selectedSubTTrack  = QComboBox     ()
        self.generateVideo      = QPushButton   ("Generate")
        # self.info               = QLabel        ("Choisissez un fichier\n")
        self.info               = ScrollLabel()
        self.progress_bar       = QProgressBar  (self)
        self.folderButton       = QPushButton   ("Open File Out Folder")
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(5)
        self.info.setText("Choisissez un fichier\n")
        self.info.setMinimumHeight(300)

        self.pathButton     .clicked.connect(self.choosefilevideo)
        self.folderButton   .clicked.connect(self.openFolder)
        self.generateVideo  .clicked.connect(self.generateVideoFinal)

        self.work_request = Signal(int)

        self.loadWorker = LoadWorker(self)
        self.worker_thread = QThread()
        self.loadWorker.progress.connect(self.update_progress)
        self.loadWorker.completed.connect(self.complete)
        self.loadWorker.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.generateWorker = GenerateWorker(self)
        self.generateThread = QThread()
        self.generateWorker.progress.connect(self.update_progress)
        self.generateWorker.completed.connect(self.complete)
        self.generateWorker.moveToThread(self.generateThread)
        self.generateThread.start()

        # LAYOUT
        layout = QGridLayout()
        layout.addWidget(self.iconVideo,            0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.labelVideo,           1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pathButton,           2, 0)
        layout.addWidget(self.iconSound,            0, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.labelSoundTrack,      1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.selectedSoundTrack,   2, 1)
        layout.addWidget(self.iconSubtt,            0, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.labelSubTTrack,       1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.selectedSubTTrack,    2, 2)
        layout.addWidget(self.generateVideo,        2, 3)
        layout.addWidget(self.info,                 3, 0, 2, 2)
        layout.addWidget(self.folderButton,         3, 2, 1, 2)
        layout.addWidget(self.progress_bar,         4, 2, 1, 2)
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
            self.addInfo(f"Fichier choisi : {folderPath[0].path()}")
            self.loadVideo(folderPath[0].path())
        except Exception as e :
            print(e)
            self.addInfo(f"ERROR : {e}")
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Error :"+str(e))
            error.setWindowTitle("Erreur de validation")
    
    def loadVideo(self, path):
        self.labelVideo.setText(path)
        self.labelVideo.update()
        self.addInfo(f"Préparation des dossiers temporaires")
        if os.path.exists(self.sf.fileout + "temp"):
            shutil.rmtree(self.sf.fileout + "temp")
        os.mkdir(self.sf.fileout + "temp")
        shutil.copy(path[1:], self.sf.fileout + "temp")
        path = self.sf.fileout + "temp/" + path.split("/")[-1]
        self.addInfo(f"Chargement de la vidéo")
        self.sf.loadVideo(path)
        self.addInfo(f"Séparation des Track")
        self.loadWorker.do_work()

    def generateVideoFinal(self):
        self.generateWorker.do_work()
        QCoreApplication.processEvents()
    
    def messageValidation(self):
        msgBox = QMessageBox()
        msgBox.setText("Video généréee avec succès")
        msgBox.setWindowTitle("SUCCESS")
        msgBox.exec()

    def addInfo(self, message):
        info = self.info.text()
        info += f"{message}\n"
        self.info.setText(info)
        self.info.update()
    
    def update_progress(self, v):
        self.progress_bar.setValue(v)
        QCoreApplication.processEvents()

    def complete(self, v):
        self.progress_bar.setValue(0)
    
    def openFolder(self):
        path = self.sf.fileout.replace('/', '\\')
        print(path)
        subprocess.Popen(f"explorer {os.getcwd()}\{path}")
