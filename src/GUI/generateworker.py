from PyQt5.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot
import shutil

class GenerateWorker(QObject):
    progress = Signal(int)
    completed = Signal(int)

    def __init__(self, gui) -> None:
        self.gui = gui
        super().__init__()

    @Slot(int)
    def do_work(self):
        self.progress.emit(0)

        self.gui.addInfo(f"préparation du merge")
        snt = int(self.gui.selectedSoundTrack.currentText().split(" - ")[0])
        sbt = self.gui.selectedSubTTrack.currentText().split(" - ")[0]
        if sbt == "":
            sbt = None
        else :
            sbt = int(sbt)
        print(snt)
        print(sbt)

        self.progress.emit(1)

        self.gui.addInfo(f"Début du merge")

        self.progress.emit(2)

        self.gui.sf.assembly_video_audio_subtitle(snt, sbt)
        self.gui.addInfo(f"SUCCESS")

        self.progress.emit(4)

        self.gui.addInfo(f"Suppression des fichiers de construction")
        print("suppression des fichiers de construction")
        shutil.rmtree(self.gui.sf.fileout + "temp")
        self.gui.selectedSoundTrack.clear()
        self.gui.selectedSubTTrack.clear()
        self.gui.labelVideo.setText("")
        self.gui.addInfo(f"SUCCESS")
        self.gui.messageValidation()

        self.completed.emit(5)