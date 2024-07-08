import threading
import time
from src.AudioPlayer import AudioPlayer
from mutagen.mp3 import MP3


class Scheduler:
    def __init__(self):
        self.scheduledAudios = {}

    def AddVideo(self, audioPath, startTime, endTime):
        time = (startTime, endTime)
        if time not in self.scheduledAudios:
            self.scheduledAudios[time] = [audioPath]
        else:
            self.scheduledAudios[time].append(audioPath)

    #checkSchedule will always need to be checking for next songs, so needs to be on separate thread
    def startBackgroundTask(self):
        thread = threading.Thread(target=self.checkSchedule, daemon=True)
        thread.start()

    def checkSchedule(self):
        while True:
            currentTime = time.strftime("%H:%M")
            print(self.scheduledAudios)
            for (startTime, endTime), audios in list(self.scheduledAudios.items()):
                if startTime <= currentTime <= endTime:
                    for audioPath in audios:
                        AudioPlayer.PlayAudio(audioPath)

            # Update the schedule every minute
            time.sleep(10)

    def getMP3Length(self, audioPath):
        audio = MP3(audioPath)
        return round(audio.info.length)