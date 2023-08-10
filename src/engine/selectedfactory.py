# from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import TextClip
from moviepy.editor import CompositeVideoClip
import subprocess

class SelectedFactory :
    def __init__(self) :
        #INIT
        self.videopath = ""
        self.fileout = "./file_out/"
    
    def loadVideo(self, video_path, output_path = "./file_out/"):
        self.videopath = video_path
        print("load")

    def info_video(self):
        """Utilise mkvinfo pour récupérer les numéros de pistes des différentes parties d'une vidéo

        Returns:
            dictionnaire: Contient les numéros de pistes servant aux exports des différentes parties d'une vidéo.
        """
        command = [
            "mkvinfo",
            self.videopath,
        ]
        pistes = {
            'video' : [],
            'subtt' : [],
            'audio' : [],
        }
        # Exécution de la commande
        run = subprocess.run(command, capture_output=True, text=True)
        print(run.stderr)
        data_run = run.stdout.split("\n")
        for i in range(len(data_run)):
            if "mkvmerge" in data_run[i]:
                if "vid" in data_run[i+2] :
                    pistes["video"] += [int(data_run[i][-2:-1])]
                elif "audio" in data_run[i+2] :
                    pistes["audio"] += [int(data_run[i][-2:-1])]
                elif "sous-titres" in data_run[i+2] :
                    pistes["subtt"] += [int(data_run[i][-2:-1])]
        return pistes
    
    def export_subtitles(self):
        """Exporte dans des fichiers les sous-titres d'une vidéo mkv grâce à mkvextract.
            fichier de sortie : temp/subtt{n}.idx et .sub
        """
        try:
            pistes = self.info_video()
            for n in pistes["subtt"] :
                command = [
                    "mkvextract",
                    "tracks",
                    self.videopath,
                    f"{n}:{self.fileout}temp/subtt{n}.srt"
                ]
                # Exécution de la commande
                run = subprocess.run(command, capture_output=True, text=True)
                print(run.stdout)
                print(run.stderr)
        except Exception as e:
            print("Une erreur s'est produite :", e)

    def export_audio_track(self):
        """Exporte les fichiers audio d'un vidéo MKV au format wav
            fichier : temp/audio{n}.wav
        """
        try:
            pistes = self.info_video()
            for n in pistes["audio"] :
                command = [
                    "mkvextract",
                    "tracks",
                    self.videopath,
                    f"{n}:{self.fileout}temp/audio{n}.wav"
                ]
                # Exécution de la commande
                run = subprocess.run(command, capture_output=True, text=True)
                print(run.stdout)
                print(run.stderr)
        except Exception as e:
            print("Une erreur s'est produite :", e)

    def export_video_track(self):
        """Exporte le fichier vidéo d'un vidéo MKV au format wav
            fichier : temp/video{n}.mkv
        """
        try:
            pistes = self.info_video()
            for n in pistes["video"] :
                command = [
                    "mkvextract",
                    "tracks",
                    self.videopath,
                    f"{n}:{self.fileout}temp/video{n}.mkv"
                ]
                # Exécution de la commande
                run = subprocess.run(command, capture_output=True, text=True)
                print(run.stdout)
                print(run.stderr)
        except Exception as e:
            print("Une erreur s'est produite :", e)
    
    def assembly_video_audio_subtitle(self, nv, nsb = None):
        # Chemin et noms des fichiers source
        video_path = f"{self.fileout}temp/video{0}.mkv"
        audio_path = f"{self.fileout}temp/audio{nv}.wav"
        

        # Chemin et nom du fichier de sortie assemblé
        output_path = f"{self.fileout}file.mkv"

        # Commande pour assembler la vidéo, la piste audio et les sous-titres avec mkvmerge
        command = [
            "mkvmerge",
            "-o", output_path,
            "--language", "0:fre", "--default-track", "0:yes", video_path,
            "--language", "0:fre", "--default-track", "0:yes", audio_path,
            # "--track-name", "0:French", "--sub-charset", "0:UTF-8", "--forced-track", "0:no", "--sub-enc", "0:UTF-8", subtitle_path
        ]

        # Exécution de la commande
        run = subprocess.run(command, capture_output=True, text=True)
        print(run.stdout)
        print(run.stderr)
        subtitle_path = ""
        if nsb != None :
            subtitle_path = f"{self.fileout}temp/subtt{nsb}.idx"
            video_path = output_path
            subtitles_path = subtitle_path

            # Chemin et nom du fichier de sortie avec les sous-titres incrustés
            output_path = f"{self.fileout}fileFinal.mkv"

            # Commande pour incruster les sous-titres IDX dans la vidéo MKV avec ffmpeg
            command = [
                "ffmpeg",
                "-i", video_path,
                "-i", subtitles_path,
                "-filter_complex", "[0:v][1:s]overlay[v]",
                "-map", "[v]",
                "-map", "0:a",
                output_path
            ]

            # Exécution de la commande
            run = subprocess.run(command, capture_output=True, text=True)
            print(run.stdout)
            print(run.stderr)
        print("Assemblage terminé avec succès.")

if __name__ == '__main__':
    sf = SelectedFactory()
    sf.loadVideo("./file_in/WINGMAN_01_SCN.Title3.mkv")
    sf.assembly_video_audio_subtitle(2, 3)
    # sf.loadVideo("./file_in/Super Gals episode 1.mp4")