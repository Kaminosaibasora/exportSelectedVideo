import subprocess

class SelectedFactory :
    def __init__(self) :
        # ========= INIT =========
        self.videopath   = ""
        self.namefile    = ""
        self.fileout     = "../file_out/"
        self.output_path = "../file_out/"
        # ========================
    
    def loadVideo(self, video_path, output_path = "../file_out/"):
        """Enregistre tous les paths nécessaires au traitement de la vidéo.
            Passe la vidéo au format MKV si ce n'est pas encore le cas.
        Args:
            video_path (str): Path complet de la vidéo
            output_path (str, optional): Emplacement de sortie par défaut de la vidéo. Defaults to "../file_out/".
        """
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
        """Convertie une vidéo au format MKV et met à jour les paths.
        """
        newvideopath = f"{self.fileout}temp/{self.namefile.split('.')[0]}.mkv"
        print(newvideopath)
        commande = [
            "ffmpeg",
            "-i", self.videopath,   # Fichier d'entrée
        ]
        run = subprocess.run(commande, capture_output=True, text=True)
        commande = [
            "ffmpeg",
            "-i", self.videopath,   # Fichier d'entrée
            "-c:v", "copy",         # Codec vidéo
            "-c:a", "copy",         # Codec audio
            "-c:s", "copy",         # piste de sous-titre
        ]
        video_data = run.stderr.split("\n")
        for line in video_data :
            if "Stream" in line and ("Video" in line or "Audio" in line or "Subtitle" in line) and not "png" in line :
                print(line)
                commande += ["-map", line[10:13]]
        commande += [newvideopath]
        run = subprocess.run(commande)
        # print(run.stdout)
        if run.stderr != "None" :
            print(f"ERROR >>> {run.stderr}")
            raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
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
            # print(run.stdout)
            if run.stderr != "" :
                print(f"ERROR >>> {run.stderr}")
                raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
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
        # print(run.stdout)
        if run.stderr != "" :
            print(f"ERROR >>> {run.stderr}")
            raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
        data_run = run.stdout.split("\n")
        for i in range(len(data_run)):
            if "mkvmerge" in data_run[i]:
                langue = ""
                j = i
                while langue == "":
                    j += 1
                    if "Langue" in data_run[j] :
                        langue = data_run[j].split(" ")[-1]
                k = 1
                while not "Type de piste" in data_run[i+k] :
                    k+=1
                if "vid" in data_run[i+k] :
                    pistes["video"] += [int(data_run[i][-2:-1])]
                elif "audio" in data_run[i+k] :
                    pistes["audio"] += [(int(data_run[i][-2:-1]), langue)]
                elif "sous-titres" in data_run[i+k] :
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
                # print(run.stdout)
                if run.stderr != "" :
                    print(f"ERROR >>> {run.stderr}")
                    raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
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
                # print(run.stdout)
                if run.stderr != "" :
                    print(f"ERROR >>> {run.stderr}")
                    raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
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
                # print(run.stdout)
                if run.stderr != "" :
                    print(f"ERROR >>> {run.stderr}")
                    raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
        except Exception as e:
            print("Une erreur s'est produite :", e)
    
    def assembly_video_audio_subtitle(self, nv, nsb = None):
        """Assemblage des différentes pistes de la vidéo finale.

        Args:
            nv (int): numéro de la piste de son
            nsb (int, optional): numéro de la piste de sous-titre. Defaults to None.
        """
        video_path  = f"{self.fileout}temp/video{0}.mkv"
        audio_path  = f"{self.fileout}temp/audio{nv}.wav"
        output_path = f"{self.fileout}temp/file.mkv"
        # Commande pour assembler la vidéoet  la piste audio et les sous-titres avec mkvmerge
        command = [
            "mkvmerge",
            "-o", output_path,
            "--language", "0:fre", "--default-track", "0:yes", video_path,
            "--language", "0:fre", "--default-track", "0:yes", audio_path,
        ]
        run = subprocess.run(command, capture_output=True, text=True)
        print(run.stdout)
        if run.stderr != "" :
            print(f"ERROR >>> {run.stderr}")
            raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
        if nsb != None :
            subtitle_path   = f"{self.fileout}temp/subtt{nsb}.idx"
            video_path      = output_path
            output_path     = f"{self.fileout}{self.namefile}"
            print(">>> "+output_path+"\nstart merge")
            # Commande pour incruster les sous-titres IDX dans la vidéo MKV avec ffmpeg
            command = [
                "ffmpeg",
                "-i", video_path,
                "-i", subtitle_path,
                "-filter_complex", "[0:v][1:s]overlay[v]",
                "-map", "[v]",
                "-map", "0:a",
                output_path
            ]
            run = subprocess.run(command, capture_output=True, text=True)
            print(run.stdout)
            if run.stderr != "" :
                print(f"ERROR >>> {run.stderr}")
                raise Exception("Convert to MKV : FAILURE \n"+run.stderr)
        print("Assemblage terminé avec succès.")
        return

if __name__ == '__main__':
    sf = SelectedFactory()
    sf.loadVideo("../file_in/WINGMAN_01_SCN.Title3.mkv")
    print(sf.info_video())
    sf.export_video_track()
    sf.export_audio_track()
    sf.export_subtitles()
    sf.assembly_video_audio_subtitle(2, 3)
    # sf.loadVideo("../file_in/Super Gals episode 1.mp4")