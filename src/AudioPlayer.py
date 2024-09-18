from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import yt_dlp
import vlc


currentPlayback = None

def playAudio(audioPath):
    global currentPlayback
    stopAudio()
    if audioPath.startswith("https://"):
        audioURL = getYouTubeInfo(audioPath)['url']
        currentPlayback = vlc.MediaPlayer(audioURL)
        currentPlayback.play()
        # implementation for YT links
    else:
        audio = AudioSegment.from_file(audioPath)
        currentPlayback = _play_with_simpleaudio(audio)


def stopAudio():
    global currentPlayback
    global videoPlayer
    if currentPlayback is not None:
        print(currentPlayback)
        currentPlayback.stop()
        print(currentPlayback)
        currentPlayback = None


# Used to extract audio stream URL and duration
def getYouTubeInfo(audioPath):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(audioPath, download=False)
        return {
            'url': info['url'],
            'duration': info['duration']
        }