# Audio Scheduler

## Overview
This project is an audio scheduler application that allows users to schedule and play audio files at specified times.
It currently supports both local MP3 files and YouTube links.

![image](https://github.com/uckkla/audio-scheduler/assets/135323891/1b6eb83a-676f-472e-adac-fa580390dae7)


## Features
- **Audio Queue**: Program correctly places each audio onto a queue, and will only repeat previous audios when every audio has been played.
- **Schedule Audio Playback**: Easily schedule MP3 files to play at the times chosen up to a certain time.
- **Audio Control**: Can schedule, stop, and remove audio from the schedule dynamically.
- **User-Friendly Interface**: Uses a simple GUI made with PyQt6 for managing the schedule.
- **Save/Load Schedule**: Option to save a schedule as a JSON and load when needed.

## Installation Guide
Clone the repository using git

```
git clone https://github.com/uckkla/audio-scheduler.git
cd audio-scheduler
```

Install requirements

```
pip install -r requirements.txt
```

Install VLC 3.0.21 or greater (Required for playing YT videos)
```
https://get.videolan.org/vlc/3.0.21/win64/vlc-3.0.21-win64.exe
```

Run Program

```
cd src
python3 main.py
```

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

## TODO
- Add a volume slider to adjust audio volume.
- Fully implement stop/continue audio playing option.
