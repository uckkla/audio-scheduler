from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


currentPlayback = None

def PlayAudio(audioPath):
    global currentPlayback
    if audioPath.startswith("https://"):
        return
        # implementation for YT links
    else:
        audio = AudioSegment.from_file(audioPath)
        StopAudio()
        currentPlayback = _play_with_simpleaudio(audio)


def StopAudio():
    global currentPlayback
    if currentPlayback is not None:

        print(currentPlayback)
        currentPlayback.stop()
        print(currentPlayback)
        currentPlayback = None
