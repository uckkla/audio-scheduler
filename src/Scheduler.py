import threading
import time
from src.AudioPlayer import PlayAudio, StopAudio
from mutagen.mp3 import MP3
from collections import deque
from threading import Event


class Scheduler:
    """
    scheduledAudios (dictionary): stores all audios that exist
    audioQueue (queue): stores what audios to be played next
    playedAudios (set): stores what songs have been played before
    """
    def __init__(self):

        self.scheduledAudios = {}
        self.audioQueue = deque()
        self.currentAudio = None
        # Stores all audios that have been previously played
        self.playedAudios = set()
        # Required for instantly starting next audio if current is removed
        self.stopEvent = threading.Event()

    def AddAudio(self, audioPath, startTime, endTime):
        time = (startTime, endTime)
        if time not in self.scheduledAudios:
            self.scheduledAudios[time] = [audioPath]
        else:
            self.scheduledAudios[time].append(audioPath)

    def RemoveAudio(self, audioPath, startTime, endTime):
        time = (startTime, endTime)
        self.scheduledAudios[time].remove(audioPath)
        # Remove audio from queue
        if audioPath in self.audioQueue:
            self.audioQueue.remove(audioPath)
        # Stop audio if current one is same as removed
        if audioPath in self.playedAudios:
            self.playedAudios.remove(audioPath)
        if audioPath == self.currentAudio:
            StopAudio()
            self.currentAudio = None
            self.stopEvent.set()

    # checkSchedule will always need to be checking for next songs, so needs to be on separate thread
    def startBackgroundTask(self):
        thread = threading.Thread(target=self.checkSchedule, daemon=True)
        thread.start()

    def checkSchedule(self):
        while True:
            self.stopEvent.clear()
            currentTime = time.strftime("%H:%M")
            print(self.scheduledAudios)
            # Add all audios that are in timeframe to queue
            for (startTime, endTime), audios in list(self.scheduledAudios.items()):
                if startTime <= currentTime <= endTime:
                    for audioPath in audios:
                        # Will only play old audios when none are left to play
                        if audioPath not in self.playedAudios:
                            self.audioQueue.append(audioPath)
                            self.playedAudios.add(audioPath)
            # Play new audio and wait until it finishes
            if self.audioQueue:
                print(self.audioQueue)
                self.currentAudio = self.audioQueue.popleft()
                StopAudio()
                PlayAudio(self.currentAudio)
                # Update schedule every minute
                sleepTime = self.getMP3Length(self.currentAudio)
                self.stopEvent.wait(timeout=sleepTime)
            else:
                self.playedAudios.clear()
                time.sleep(1)

    def getMP3Length(self, audioPath):
        audio = MP3(audioPath)
        return round(audio.info.length)