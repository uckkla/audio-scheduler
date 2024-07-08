from pydub import AudioSegment
from pydub.playback import play

class AudioPlayer:

    def PlayAudio(audioPath):
        if audioPath.startswith("https://"):
            return
            # implementation for YT links
        else:
            audio = AudioSegment.from_mp3(audioPath)
            play(audio)
