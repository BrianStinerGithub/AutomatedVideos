from __future__ import unicode_literals
import moviepy.editor as mpy
import os
import time

import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

# ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "ultrafast"
vcodec =   "libx264"
videoquality = "24"

txt_dir, audio_dir, playlist_url = "description/tracklist.txt", "audio", "https://www.youtube.com/playlist?list=PLKOse5kqL5dDMwOUqqs4pmk_cFx3Pk17H"

def download_audio(description_dir, audio_dir, playlist_url):

    # load description
    tracklist = open(description_dir, "w")
    tracklist.write("\n")
    tracklist.write("Tracklist  • • • ")
    tracklist.write("\n")

    # download songs from list.txt
    ydl_opts = {
    'format': 'bestaudio/best',
    'filename': '~/audio/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

    # load songs and add tracklist to description
    duration, i = 0, 1
    for file in os.listdir(audio_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".mp3") or filename.endswith(".m4a"):
            current_song = mpy.AudioFileClip(os.path.join(audio_dir, filename))
            result = time.gmtime(duration)
            tracklist.write(f'{result.tm_hour}:{result.tm_min}:{result.tm_sec} • {filename.split(".")[0]} \n')
            os.rename(os.path.join(audio_dir, filename), os.path.join(audio_dir, "audio"+i+".mp3"))
            i=i+1
            duration += current_song.duration


if __name__ == '__main__':
    download_audio(txt_dir, audio_dir, playlist_url)