import subprocess

class SelectedFactory :
    def __init__(self) :
        # ========= INIT =========
        self.videopath   = ""
        self.namefile    = ""
        self.fileout     = "./file_out/"
        self.output_path = "./file_out/"
        # ========================
    
    def loadVideo(self, video_path, output_path = "./file_out/"):
        self.videopath   = video_path
        self.output_path = output_path
        self.namefile = video_path.split("/")[-1]
        if not self.isMkvVideo():
            self.convertVideoToMkv()
        print(f"LOAD\nvideo : {self.namefile}")
    
    def isMkvVideo(self):
        if self.namefile.split(".")[-1] != "mkv":
            return False
        return True

    def convertVideoToMkv(self):
        # TODO : trouver un moyen pour automatiser la détection des pistes audio et de sous-titre
        newvideopath = f"{self.fileout}temp/{self.namefile.split('.')[0]}.mkv"
        print(newvideopath)
        commande = [
            "ffmpeg",
            "-i", self.videopath,   # Fichier d'entrée
            "-c:v", "copy",         # Codec vidéo
            "-c:a", "copy",         # Codec audio
            "-c:s", "copy",         # piste de sous-titre
            "-map", "0:0",
            "-map", "0:1",
            "-map", "0:2",
            "-map", "0:3",
            "-map", "0:4",
            newvideopath # Fichier de sortie au format MKV
        ]
        run = subprocess.run(commande)
        print(run.stdout)
        print(run.stderr)
        self.videopath = newvideopath
        self.namefile = f"{self.namefile.split('.')[0]}.mkv"
        print("Convert effected")

    def info_video(self):
        """Utilise mkvinfo pour récupérer les numéros de pistes des différentes parties d'une vidéo

        Returns:
            dictionnaire: Contient les numéros de pistes servant aux exports des différentes parties d'une vidéo.
        """
        if ":" in self.videopath:
            print(self.videopath[1:3])
            command = [self.videopath[1:3]]
            run = subprocess.run(command, capture_output=True, text=True)
            print(run.stdout)
            print(run.stderr)
            self.videopath = self.videopath[4:]
            print(self.videopath)
        command = [
            "mkvinfo",
            self.videopath,
        ]
        pistes = {
            'video' : [],
            'subtt' : [],
            'audio' : [],
        }
        run = subprocess.run(command, capture_output=True, text=True)
        print(run.stdout)
        print(run.stderr)
        data_run = run.stdout.split("\n")
        for i in range(len(data_run)):
            if "mkvmerge" in data_run[i]:
                langue = ""
                j = i
                while langue == "":
                    j += 1
                    if "Langue" in data_run[j] :
                        langue = data_run[j].split(" ")[-1]
                if "vid" in data_run[i+2] :
                    pistes["video"] += [int(data_run[i][-2:-1])]
                elif "audio" in data_run[i+2] :
                    pistes["audio"] += [(int(data_run[i][-2:-1]), langue)]
                elif "sous-titres" in data_run[i+2] :
                    pistes["subtt"] += [(int(data_run[i][-2:-1]), langue)]
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
                    f"{n[0]}:{self.fileout}temp/subtt{n[0]}.srt"
                ]
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
                    f"{n[0]}:{self.fileout}temp/audio{n[0]}.wav"
                ]
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
                run = subprocess.run(command, capture_output=True, text=True)
                print(run.stdout)
                print(run.stderr)
        except Exception as e:
            print("Une erreur s'est produite :", e)
    
    def assembly_video_audio_subtitle(self, nv, nsb = None):
        video_path  = f"{self.fileout}temp/video{0}.mkv"
        audio_path  = f"{self.fileout}temp/audio{nv}.wav"
        output_path = f"{self.fileout}file.mkv"
        # Commande pour assembler la vidéo, la piste audio et les sous-titres avec mkvmerge
        command = [
            "mkvmerge",
            "-o", output_path,
            "--language", "0:fre", "--default-track", "0:yes", video_path,
            "--language", "0:fre", "--default-track", "0:yes", audio_path,
        ]
        run = subprocess.run(command, capture_output=True, text=True)
        print(run.stdout)
        print(run.stderr)
        subtitle_path = ""
        if nsb != None :
            subtitle_path   = f"{self.fileout}temp/subtt{nsb}.idx"
            video_path      = output_path
            subtitles_path  = subtitle_path
            output_path     = f"{self.fileout}fileFinal.mkv"
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
            run = subprocess.run(command, capture_output=True, text=True)
            print(run.stdout)
            print(run.stderr)
        print("Assemblage terminé avec succès.")

if __name__ == '__main__':
    sf = SelectedFactory()
    sf.loadVideo("./file_in/WINGMAN_01_SCN.Title3.mkv")
    print(sf.info_video())
    # sf.assembly_video_audio_subtitle(2, 3)
    # sf.loadVideo("./file_in/Super Gals episode 1.mp4")