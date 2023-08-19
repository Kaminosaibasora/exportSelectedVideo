import typing
from PyQt5.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot

class LoadWorker(QObject):
    progress = Signal(int)
    completed = Signal(int)

    def __init__(self, gui) -> None:
        self.gui = gui
        super().__init__()

    @Slot(int)
    def do_work(self):
        self.progress.emit(0)

        self.gui.addInfo(f"Récupération des infos")
        infoVideo = self.gui.sf.info_video()
        print(infoVideo)
        
        self.progress.emit(1)

        itemST = []
        for i in infoVideo['audio'] :
            itemST += [f"{i[0]} - {i[1]}"]
        self.gui.selectedSoundTrack.addItems(itemST)
        itemST = [""]
        for i in infoVideo['subtt'] :
            itemST += [f"{i[0]} - {i[1]}"]
        self.gui.selectedSubTTrack.addItems(itemST)
        self.gui.addInfo(f"Success")

        self.progress.emit(2)

        self.gui.addInfo(f"Export video")
        self.gui.sf.export_video_track()

        self.progress.emit(3)

        self.gui.addInfo(f"Export audio")
        self.gui.sf.export_audio_track()

        self.progress.emit(4)

        self.gui.addInfo(f"Export Subtitles")
        self.gui.sf.export_subtitles()
        self.gui.addInfo(f"SUCCESS")

        self.progress.emit(5)

        self.completed.emit(5)