from moviepy.video.io.VideoFileClip import VideoFileClip
import subprocess

class SelectedFactory :
    def __init__(self) :
        #INIT
        self.videopath = ""
        self.fileout = "./file_out/"
    
    def loadVideo(self, video_path, output_path = "./file_out/"):
        self.videopath = video_path
        print("load")
        self.export_subtitles()
        # self.export_audio_track()
    
    def export_subtitles(self):
        try:
            cmd = ['ffmpeg', '-i', self.videopath, '-map', '0:s:0', self.fileout + "temp/file.srt"]
            # Exécution de la commande ffmpeg
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Sous-titres extraits avec succès !")

        except Exception as e:
            print("Une erreur s'est produite :", e)

    def export_audio_track(self):
        try:
            video_clip = VideoFileClip(self.videopath)
            audio_tracks = video_clip.audio.to_soundarray()
            for track_index, track in enumerate(audio_tracks.T):
                output_path = f"{self.fileout}/temp/piste_audio_{track_index + 1}.wav"
                track.write_audiofile(output_path, fps=video_clip.fps)
                print(f"Piste audio {track_index + 1} exportée avec succès !")
        except Exception as e:
            print("Une erreur s'est produite :", e)

if __name__ == '__main__':
    sf = SelectedFactory()
    # sf.loadVideo("./file_in/WINGMAN_01_SCN.Title3.mkv")
    sf.loadVideo("./file_in/Super Gals episode 1.mp4")