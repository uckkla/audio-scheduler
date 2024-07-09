# Audio Scheduler

## Overview
This project is an audio scheduler application that allows users to schedule and play audio files at specified times.
It currently supports local MP3 files, but will later work for YouTube links as well.

## Features
- **Audio Queue**: Program correctly places each audio onto a queue, and will only repeat previous audios when every audio has been played.
- **Schedule Audio Playback**: Easily schedule MP3 files to play at the times chosen up to a certain time.
- **Audio Control**: Can schedule, stop, and remove audio from the schedule dynamically.
- **User-Friendly Interface**: Uses a simple GUI made with PyQt6 for managing the schedule.

## Installation Guide
Clone the repository using git

`https://github.com/uckkla/audio-scheduler.git
cd audio-scheduler`

Install requirements

`pip install -r requirements.txt`

Run Program

`python3 main.py`

## KNOWN ISSUE
There is a bug with pydub where it fails to load the MP3 file due to having denied permissions. If so, navigate to the playback.py package within pydub and add `f.close` in the `_play_with_ffplay` function as shown:

```
def _play_with_ffplay(seg):
    PLAYER = get_player_name()
    with NamedTemporaryFile("w+b", suffix=".wav") as f:
        f.close()
        seg.export(f.name, "wav")
        subprocess.call([PLAYER, "-nodisp", "-autoexit", "-hide_banner", f.name])
```
